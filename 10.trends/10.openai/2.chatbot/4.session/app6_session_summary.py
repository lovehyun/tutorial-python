import os
import time
import logging
import sqlite3
import json

from flask import Flask, request, send_from_directory, jsonify, g
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='public')  # 정적 파일 폴더 설정
CORS(app)  # Cross-Origin Resource Sharing 설정
port = int(os.environ.get('PORT', 5000))


# DB 가져오는 코드 - 연결 및 접속 종료
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('history.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# SQLite 쿼리 결과를 딕셔너리 형태로 변환하는 함수
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# OpenAI 셋업
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Create a client instance
client = OpenAI(api_key=openai_api_key)

# logging 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 대화 히스토리 및 세션 테이블 생성
def init_db():
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS conversation (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, role TEXT, content TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS session (id INTEGER PRIMARY KEY AUTOINCREMENT, start_time DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()

init_db()


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# 사용자의 대화를 받아 처리하고 챗봇 응답을 반환
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        start = time.time() * 1000  # 요청 시작 시간 기록
        session_id = request.json['sessionId']
        user_input = request.json['userInput']
        print(f' => 사용자 요청: {user_input}')

        # 대화 내용 DB에 추가
        with app.app_context():
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO conversation (session_id, role, content) VALUES (?, ?, ?)", (session_id, 'user', user_input))
            conn.commit()

            # 기존: 최근 10개만 가져오던 코드를 전체 대화 기록을 가져오도록 변경
            # recent_conversation = get_recent_conversation(session_id)
            # formatted_conversation = [{'role': row['role'], 'content': row['content']} for row in recent_conversation]
            full_conversation = get_conversation_by_session(session_id)
            formatted_conversation = [{'role': row['role'], 'content': row['content']} for row in full_conversation]
            print(f' => 실제(프롬프트) 요청: {formatted_conversation}')

            # ChatGPT에 대화 내용 전송 (여기서 내부적으로 요약 로직이 동작합니다)
            chatgpt_response = get_chat_gpt_response(formatted_conversation)

            # 응답 결과를 DB에 추가
            cursor.execute("INSERT INTO conversation (session_id, role, content) VALUES (?, ?, ?)", (session_id, 'assistant', chatgpt_response))
            conn.commit()

        end = time.time() * 1000  # 응답 완료 시간 기록
        print(f' <= ChatGPT 응답: {chatgpt_response}')
        print(f' == 요청 및 응답 시간: {end - start} ms')

        return jsonify({'chatGPTResponse': chatgpt_response})
    except Exception as e:
        print('Error processing chat request:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# 최근 10개의 대화 내용 가져오기 (이전 방식 – 현재는 사용하지 않음)
def get_recent_conversation(session_id):
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory  # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM conversation WHERE session_id = ? ORDER BY id DESC LIMIT 10", [session_id])
        rows = cursor.fetchall()
        print(rows)

        return rows[::-1]


# 현재 세션의 전체 대화 내용 가져오기 (오름차순)
def get_conversation_by_session(session_id):
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory  # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM conversation WHERE session_id = ? ORDER BY id DESC", (session_id,))
        conversation_history = cursor.fetchall()
        return conversation_history[::-1]


# ChatGPT에 전송할 대화 내용 구성
def get_chat_gpt_response(conversation_history):
    try:
        # 기본 시스템 프롬프트
        system_prompt = {'role': 'system', 'content': 'You are a helpful assistant.'}

        # 개선된 시스템 프롬프트: 대화 내용을 기억하고, 메시지 개수를 추적하라는 지시 포함
        # system_prompt = {
        #     'role': 'system',
        #     'content': (
        #         "You are a helpful assistant. Remember all the conversation details provided below. "
        #         "Keep track of the total number of messages as well as the number of user messages, "
        #         "especially those that are questions. When the user asks about the conversation or "
        #         "message counts, answer accurately based on the conversation context. "
        #         "Do not mention that you are using any summarization or truncation of the conversation."
        #     )
        # }
        
        # 메타정보 계산: 전체 메시지 개수, 사용자 질문 개수 (끝에 '?'가 있으면 질문으로 간주)
        total_messages = len(conversation_history)
        user_questions = sum(1 for msg in conversation_history 
                             if msg['role'] == 'user' and msg['content'].strip().endswith('?'))
        meta_info = f"현재까지 대화 메시지 개수: {total_messages}개, 사용자 질문 개수: {user_questions}개."
        meta_prompt = {'role': 'system', 'content': meta_info}
        
        # 만약 전체 대화 기록이 10개 이하라면 그대로 사용
        if len(conversation_history) <= 10:
            input_messages = [system_prompt, meta_prompt] + conversation_history
            print(f"최근 대화: {input_messages}")
        else:
            # 마지막 10개의 메시지는 그대로 사용
            recent_messages = conversation_history[-10:]
            # 나머지 이전 메시지들은 요약 대상
            old_messages = conversation_history[:-10]

            # 10개 단위로 chunking하여 요약
            summaries = []
            for i in range(0, len(old_messages), 10):
                chunk = old_messages[i:i+10]
                summary_text = summarize_conversation(chunk)
                # 요약 메시지는 시스템 역할로 추가 (기존 시스템 프롬프트 이후에 추가됨)
                summaries.append({'role': 'system', 'content': f"대화 요약: {summary_text}"})

            input_messages = [system_prompt, meta_prompt] + summaries + recent_messages
            print(f"대화 요약: {summaries}")

        print("GPT에 전달할 메시지:")
        for msg in input_messages:
            print(f"{msg['role']}: {msg['content']}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_messages,
            temperature=1.0  # 예시 값: 0.7 (0.0 ~ 2.0 범위, 기본값은 1.0)
        )

        chatgpt_response = response.choices[0].message.content
        return chatgpt_response
    except Exception as e:
        print('Error making ChatGPT API request:', str(e))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'


# 대화 chunk(10개 단위)를 요약하는 함수
def summarize_conversation(conversation_chunk):
    try:
        prompt = "다음 대화 내용을 간략하게 요약해줘:\n\n"
        for msg in conversation_chunk:
            prompt += f"{msg['role']}: {msg['content']}\n"

        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 훌륭한 요약 전문가야."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        summary = summary_response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print("Error summarizing conversation:", str(e))
        return "요약 정보를 가져오는 도중에 오류가 발생했습니다."


# 최근 10개의 대화 내용을 JSON으로 반환
@app.route('/api/history')
def get_history():
    try:
        # 모든 세션의 대화 내용을 가져오기
        conversation_history = get_conversation_all_sessions()
        return json.dumps({'conversationHistory': conversation_history}, ensure_ascii=False)
    except Exception as e:
        print('Error getting recent conversation:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# 세션별 대화 내용 가져오기
def get_conversation_all_sessions():
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory  # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM conversation ORDER BY id DESC")
        rows = cursor.fetchall()
        return rows[::-1]


# 새로운 세션 시작
@app.route('/api/new-session', methods=['POST'])
def new_session():
    try:
        with app.app_context():
            conn = get_db()
            cursor = conn.cursor()

            result = cursor.execute("INSERT INTO session (start_time) VALUES (CURRENT_TIMESTAMP)")
            session_id = result.lastrowid  # 새로 생성된 세션의 ID 가져오기
            conn.commit()
            return jsonify({'success': True, 'message': 'New session started successfully.', 'sessionId': session_id})
    except Exception as e:
        print('Error starting new session:', str(e))
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500


# 현재 세션을 가져오거나 새로 생성
def get_current_session():
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory  # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT id, start_time FROM session ORDER BY start_time DESC LIMIT 1")
        current_session = cursor.fetchone()

        if not current_session:
            cursor.execute("INSERT INTO session DEFAULT VALUES")
            conn.commit()
            cursor.execute("SELECT id, start_time FROM session ORDER BY start_time DESC LIMIT 1")
            current_session = cursor.fetchone()
        
        print(current_session)
        return current_session


# 현재 세션의 대화 내용 가져오기
@app.route('/api/current-session', methods=['GET'])
def current_session():
    try:
        # 세션이 없으면 새로운 세션 시작
        current_session = get_current_session()
        conversation_history = get_conversation_by_session(current_session['id'])
        return jsonify({'conversationHistory': conversation_history, 'id': current_session['id'], 'start_time': current_session['start_time']})

    except Exception as e:
        print('Error getting current session:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# 모든 세션 가져오기
@app.route('/api/all-sessions', methods=['GET'])
def all_sessions():
    try:
        all_sessions = get_all_sessions()
        return jsonify({'allSessions': all_sessions})
    except Exception as e:
        print('Error getting all sessions:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# 최근 세션을 포함한 모든 세션 가져오기
def get_all_sessions():
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory  # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT id, start_time FROM session ORDER BY start_time DESC")
        all_sessions = cursor.fetchall()
        print(all_sessions)
        return all_sessions


# 특정 세션의 대화 내용 가져오기
@app.route('/api/session/<int:sessionId>', methods=['GET'])
def specific_session(sessionId):
    try:
        current_session = get_specific_session(sessionId)
        conversation_history = get_conversation_by_session(sessionId)
        return jsonify({'conversationHistory': conversation_history, 'id': current_session['id'], 'start_time': current_session['start_time']})
    except Exception as e:
        print('Error getting session:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# 세션별 대화 내용 가져오기
def get_specific_session(session_id):
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory  # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT id, start_time FROM session WHERE id = ?", (session_id,))
        specific_session = cursor.fetchone()
        return specific_session


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
