from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid
import requests

load_dotenv()
app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 이미지 저장 디렉토리 설정
FLASK_PUBLIC_DIR = os.path.join(os.getcwd(), 'public')
FLASK_HOST = 'localhost'
FLASK_PORT = 5000

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    message = data.get('message', '')
    task_id = data.get('taskId', 'unknown')

    print(f'[F1] 받은 메시지: {message} (작업 ID: {task_id})')

    try:
        if message.lower().startswith("이미지:") or message.lower().startswith("image:"):
            prompt = message.split(":", 1)[1].strip()
            print(f'[F2] DALL·E 이미지 생성 요청: {prompt}')

            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )

            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            print(f'[F3] DALL·E 원본 이미지 URL: {image_url}')

            filename = f"{uuid.uuid4().hex}.png"
            save_path = os.path.join(FLASK_PUBLIC_DIR, filename)
            os.makedirs(FLASK_PUBLIC_DIR, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(image_data)

            public_url = f"http://{FLASK_HOST}:{FLASK_PORT}/public/{filename}"
            print(f'[F3] 이미지 저장 및 경로: {public_url}')

            return jsonify({ 'response_type': 'image', 'image_url': public_url })

        # 일반 텍스트 처리
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
        return jsonify({ 'response_type': 'text', 'answer': answer })

    except Exception as e:
        print(f'[F4] 오류 발생:', e)
        return jsonify({ 'response_type': 'error', 'error': str(e)}), 500

# Flask에서 public 폴더 서빙
@app.route('/public/<filename>')
def serve_image(filename):
    return send_from_directory(FLASK_PUBLIC_DIR, filename)

if __name__ == '__main__':
    print(f"🟢 Flask 서버 실행 중: http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT)
