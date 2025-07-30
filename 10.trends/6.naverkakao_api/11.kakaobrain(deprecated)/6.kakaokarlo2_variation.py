import requests
import json
import io
import base64
import urllib
from PIL import Image

# REST API 키
REST_API_KEY = os.getenv("KAKAO_RESTAPI_KEY")

# Base64 인코딩 함수
def imageToString(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img

# 이미지 변환하기
def variations(image):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/variations',
        json = {
            'version': 'v2.1',
            'image': image,
            'height': 1024,
            'width': 1024
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    response = json.loads(r.content)
    return response

# 이미지 파일 불러오기
img = Image.open('original.png')

# 이미지를 Base64 인코딩하기
img_base64 = imageToString(img)

# 이미지 변환하기 REST API 호출
response = variations(img_base64)

# 응답의 첫 번째 이미지 생성 결과 출력하기
image_url = response.get("images")[0].get("image")
result = Image.open(urllib.request.urlopen(image_url))
result.show()

# 이미지 파일로 저장하기
result.save("variations_image.png")
