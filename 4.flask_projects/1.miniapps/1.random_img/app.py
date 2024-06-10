from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# 강아지 사진 URL 리스트
dog_images = [
    "https://example.com/dog1.jpg",
    "https://example.com/dog2.jpg",
    "https://example.com/dog3.jpg",
    "https://example.com/dog4.jpg",
    "https://example.com/dog5.jpg",
    "https://example.com/dog6.jpg",
    "https://example.com/dog7.jpg",
    "https://example.com/dog8.jpg",
    "https://example.com/dog9.jpg",
    "https://example.com/dog10.jpg",
]

@app.route("/random-dog")
def random_dog():
    # 강아지 사진 URL 중에서 랜덤으로 하나 선택
    random_url = random.choice(dog_images)
    # JSON 형식으로 응답 반환
    return jsonify({"url": random_url})

if __name__ == "__main__":
    app.run(debug=True)
