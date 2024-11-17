from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import json
import urllib
from PIL import Image
import io
import base64
from dotenv import load_dotenv, find_dotenv
import os

# Flask 애플리케이션 초기화
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# .env 파일에서 환경 변수 로드
load_dotenv(find_dotenv('../.env'))

# REST API 키
REST_API_KEY = os.getenv("KAKAO_RESTAPI_KEY")

# Base64 인코딩 함수
def imageToString(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img

# 이미지 생성 함수
def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            "version": "v2.1", 
            "prompt": prompt,
            "negative_prompt": negative_prompt, 
            "height": 1024,
            "width": 1024
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    response = json.loads(r.content)
    return response

# 라우트 설정
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        negative_prompt = ""

        if not prompt or len(prompt) > 2048:
            flash('Prompt is required and must be less than 2048 characters.')
            return redirect(url_for('index'))

        response = t2i(prompt, negative_prompt)
        image_url = response.get("images")[0].get("image")
        return render_template('index.html', image_url=image_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
