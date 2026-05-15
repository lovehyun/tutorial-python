import os
import time
import logging

from flask import Flask, request, send_from_directory, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='public')
port = int(os.environ.get("PORT", 5000))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    start = time.time() * 1000
    user_input = request.json.get('userInput', '')
    print(f' => [사용자 요청]: {user_input}')

    chatgpt_response = get_chatgpt_response(user_input)
    
    end = time.time() * 1000
    print(f' <= [ChatGPT 응답]: {chatgpt_response}')
    print(f'    (요청 및 응답 시간: {end - start} ms)')
    
    return jsonify({'chatGPTResponse': chatgpt_response})

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

def get_chatgpt_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                # {"role": "system", "content": "You are a first-class hotel chef providing culinary recommendations."},
                # {"role": "system", "content": "You are a travel guide providing assistance and information for travelers."},
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                # {"role": "system", "content": "당신은 최고급 호텔의 요리사로서 요리와 관련된 추천을 제공합니다."},
                # {"role": "system", "content": "당신은 여행자들에게 도움과 정보를 제공하는 여행 가이드입니다."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as error:
        print('Error making ChatGPT API request:', str(error))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
