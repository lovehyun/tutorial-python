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

            # 위 질문을 포함한, 최근 10개 대화 내용 가져오기
            recent_conversation = get_recent_conversation(session_id)

            # 필요한 필드만 선택하고 딕셔너리 리스트로 변환
            formatted_conversation = [{'role': row['role'], 'content': row['content']} for row in recent_conversation]
            print(f' => 실제(프롬푸트) 요청: {formatted_conversation}')

            # ChatGPT에 대화 내용 전송
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


# 최근 10개의 대화 내용 가져오기
def get_recent_conversation(session_id):
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM conversation WHERE session_id = ? ORDER BY id DESC LIMIT 10", [session_id])
        rows = cursor.fetchall()
        print(rows)

        return rows[::-1]


# ChatGPT에 전송할 대화 내용 구성
def get_chat_gpt_response(conversation_history):
    try:
        input_messages = [
            # 'system' 역할을 사용하여 사용자와 챗봇 간의 대화를 초기화합니다.
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            *conversation_history
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_messages
        )

        chatgpt_response = response.choices[0].message.content
        return chatgpt_response
    except Exception as e:
        print('Error making ChatGPT API request:', str(e))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'


# 최근 10개의 대화 내용을 JSON으로 반환
@app.route('/api/history')
def get_history():
    try:
        # 모든 세션의 대화 내용을 가져오기
        conversation_history = get_conversation_all_sessions()
        # return jsonify({'conversationHistory': recent_conversation})
        return json.dumps({'conversationHistory': conversation_history}, ensure_ascii=False)
    except Exception as e:
        print('Error getting recent conversation:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500


# 세션별 대화 내용 가져오기
def get_conversation_all_sessions():
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory # 딕셔너리로 변환
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
        conn.row_factory = dict_factory # 딕셔너리로 변환
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


# 세션별 대화 내용 가져오기
def get_conversation_by_session(session_id):
    with app.app_context():
        conn = get_db()
        conn.row_factory = dict_factory # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM conversation WHERE session_id = ? ORDER BY id DESC", (session_id,))
        conversation_history = cursor.fetchall()
        return conversation_history[::-1]


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
        conn.row_factory = dict_factory # 딕셔너리로 변환
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
        conn.row_factory = dict_factory # 딕셔너리로 변환
        cursor = conn.cursor()

        cursor.execute("SELECT id, start_time FROM session WHERE id = ?", (session_id,))
        specific_session = cursor.fetchone()
        return specific_session


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
