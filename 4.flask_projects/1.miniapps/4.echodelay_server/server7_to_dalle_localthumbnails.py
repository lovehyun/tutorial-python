# bash: curl -X POST http://localhost:5000/process -H "Content-Type: application/json; charset=utf-8" -d '{"message": "이미지: 귀여운 강아지가 초원에서 놀고 있는 그림", "taskId": "test123"}'

# pip install flask flask-cors openai python-dotenv requests pillow
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import os
import uuid
import requests
from io import BytesIO

load_dotenv()
app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 디렉토리 설정
FLASK_PUBLIC_DIR = os.path.join(os.getcwd(), 'public')
IMAGES_DIR = os.path.join(FLASK_PUBLIC_DIR, 'images')
THUMBS_DIR = os.path.join(FLASK_PUBLIC_DIR, 'thumbnails')
FLASK_HOST = 'localhost'
FLASK_PORT = 5000

# 디렉토리 생성
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(THUMBS_DIR, exist_ok=True)

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
            print(f'[F3] DALL·E 원본 이미지 URL: {image_url}')
            image_data = requests.get(image_url).content

            # 파일 이름 생성
            filename = f"{uuid.uuid4().hex}.png"
            image_path = os.path.join(IMAGES_DIR, filename)
            thumb_path = os.path.join(THUMBS_DIR, filename)

            # 원본 저장
            with open(image_path, 'wb') as f:
                f.write(image_data)
            print(f'[F4] 원본 이미지 저장: {image_path}')

            # 썸네일 생성 및 저장
            image = Image.open(BytesIO(image_data))
            image.thumbnail((128, 128))
            image.save(thumb_path)
            print(f'[F5] 썸네일 저장: {thumb_path}')

            # URL 생성
            public_image_url = f"http://{FLASK_HOST}:{FLASK_PORT}/public/images/{filename}"
            public_thumb_url = f"http://{FLASK_HOST}:{FLASK_PORT}/public/thumbnails/{filename}"

            return jsonify({
                'response_type': 'image',
                'image_url': public_image_url,
                'thumbnail_url': public_thumb_url
            })

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
        print(f'[F6] 오류 발생:', e)
        return jsonify({ 'response_type': 'error', 'error': str(e)}), 500

# 정적 파일 서빙
@app.route('/public/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/public/thumbnails/<filename>')
def serve_thumbnail(filename):
    return send_from_directory(THUMBS_DIR, filename)

if __name__ == '__main__':
    print(f"🟢 Flask 서버 실행 중: http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT)
