import requests
import json
import urllib
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# REST API 키
REST_API_KEY = os.getenv("KAKAO_RESTAPI_KEY")

# Base64 인코딩 함수
def imageToString(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img

# 이미지 생성하기
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

# 프롬프트에 사용할 제시어
prompt = "A photo of a cute tiny monster on the beach, daylight."
negative_prompt = ""

# 이미지 생성하기 REST API 호출
response = t2i(prompt, negative_prompt)

# 응답의 첫 번째 이미지 생성 결과 출력하기
image_url = response.get("images")[0].get("image")
result = Image.open(urllib.request.urlopen(image_url))
result.show()

# 이미지 파일로 저장하기
result.save("generated_image.png")
