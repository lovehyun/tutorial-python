from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    message = data.get('message', '')
    task_id = data.get('taskId', 'unknown')

    print(f'[F1] 받은 메시지: {message} (작업 ID: {task_id})')

    try:
        # 이미지 요청일 경우
        if message.lower().startswith("이미지:") or message.lower().startswith("image:"):
            prompt = message.split(":", 1)[1].strip()
            print(f'[F2] DALL·E 이미지 생성 요청: {prompt}')

            response = client.images.generate(
                model="dall-e-3",  # 또는 "dall-e-2"
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            image_url = response.data[0].url
            print(f'[F3] 이미지 생성 완료 (ID: {task_id}): {image_url}')
            return jsonify({ 'response_type': 'image', 'image_url': image_url })

        # 일반 텍스트 챗 요청
        else:
            print(f'[F2] GPT 채팅 요청: {message}')
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    { "role": "system", "content": "You are a helpful assistant." },
                    { "role": "user", "content": message }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            answer = response.choices[0].message.content.strip()
            print(f'[F3] GPT 응답 완료 (ID: {task_id}): {answer}')
            return jsonify({ 'response_type': 'text', 'answer': answer })

    except Exception as e:
        print(f'[F4] 오류 발생:', e)
        return jsonify({ 'response_type': 'error', 'error': str(e) }), 500

if __name__ == '__main__':
    print('🟢 Flask 서버 실행 중: http://localhost:5000')
    app.run(port=5000)
