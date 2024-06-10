from flask import Flask, jsonify, url_for, send_from_directory
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# 이미지 파일이 저장된 디렉토리 경로
# IMAGE_FOLDER = './static/images'

# 강아지 사진 URL 리스트
dog_images = [
    # "https://example.com/dog1.jpg",
    # "https://example.com/dog2.jpg",
    # "https://example.com/dog3.jpg",
    # "https://example.com/dog4.jpg",
    # "https://example.com/dog5.jpg",
    # "https://example.com/dog6.jpg",
    # "https://example.com/dog7.jpg",
    # "https://example.com/dog8.jpg",
    # "https://example.com/dog9.jpg",
    # "https://example.com/dog10.jpg",
    "cat1.jpg",
    "cat2.jpg",
    "cat3.jpg",
]

@app.route("/random-dog")
def random_dog():
    # 강아지 사진 URL 중에서 랜덤으로 하나 선택
    random_image  = random.choice(dog_images)
    # 파일 URL 생성
    image_url = url_for('static', filename=f'images/{random_image}', _external=True)
    
    # static 이 아닌 다른 폴더에서 서빙하는 경우
    # image_url = url_for('serve_image', filename=random_image, _external=True)
    
    # JSON 형식으로 응답 반환
    return jsonify({"url": image_url})

# @app.route('/images/<filename>')
# def serve_image(filename):
#     return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
