from flask import Flask, request, send_from_directory, jsonify
import openai
from dotenv import load_dotenv
import os
import time
import logging
import json

load_dotenv()

app = Flask(__name__, static_folder='public')  # 정적 파일 폴더 설정
port = int(os.environ.get("PORT", 5000))

# OpenAI 셋업
openai.api_key = os.environ.get("OPENAI_API_KEY")

# logging 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 콘솔에 사용자의 요청과 챗봇 응답 출력
# @app.before_request
# def log_request():
#     if request.method == 'POST':
#         logger.info('=> 사용자 요청: %s', request.json.get('userInput', ''))

# 대화 히스토리 길이 관리
MAX_HISTORY_LENGTH = 10

# 이전 대화 내용을 저장할 리스트
conversation_history = []
conversation_seq = 0


@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    global conversation_seq

    start = time.time() * 1000  # 요청 시작 시간 기록
    user_input = request.json.get('userInput', '')
    print(f' => 사용자 요청: {user_input}')

    # 이전 대화 내용 추가
    conversation_history.append({'role': 'user', 'content': user_input})
    conversation_seq += 1
    print(f' => 실제(프롬푸트) 요청: {conversation_history}')

    # ChatGPT에 대화 내용 전송
    chatgpt_response = get_chatgpt_response(conversation_history)

    end = time.time() * 1000  # 응답 완료 시간 기록
    print(f' <= ChatGPT 응답: {chatgpt_response}')
    print(f' == 요청 및 응답 시간: {end - start} ms')

    # 이전 대화 내용에 ChatGPT 응답 추가
    conversation_history.append({'role': 'assistant', 'content': chatgpt_response})
    conversation_seq += 1

    # 대화 히스토리 길이 관리
    while len(conversation_history) > MAX_HISTORY_LENGTH:
        conversation_history.pop(0)  # 가장 오래된 대화들 삭제

    return jsonify({'chatGPTResponse': chatgpt_response})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# 수동으로 과거 대화내용 확인하는 API
@app.route('/api/history')
def get_history():
    global conversation_history
    global conversation_seq

    # 대화 히스토리에 번호 추가
    numbered_history = [
        {'role': item['role'], 'content': item['content'], 'number': conversation_seq - (len(conversation_history) - index) + 1}
        for index, item in enumerate(conversation_history)
    ]

    # return jsonify({'conversationHistory': numbered_history})
    return json.dumps({'conversationHistory': numbered_history}, ensure_ascii=False)


# ChatGPT에 전송할 대화 내용 구성
def get_chatgpt_response(conversation_history):
    try:
        # 'system' 역할을 사용하여 사용자와 챗봇 간의 대화를 초기화합니다.
        input_messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            # {'role': 'system', 'content': 'You are a first-class hotel chef providing culinary recommendations.'},
            # {'role': 'system', 'content': 'You are a travel guide providing assistance and information for travelers.'},
            *conversation_history,
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=input_messages
        )

        chatgpt_response = response['choices'][0]['message']['content']
        # logger.info('ChatGPT 응답: %s', chatgpt_response)
        return chatgpt_response

    except Exception as error:
        logger.error('Error making ChatGPT API request: %s', str(error))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
