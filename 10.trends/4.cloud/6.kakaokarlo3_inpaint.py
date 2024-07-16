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

# 이미지 편집하기
def inpainting(image, mask):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/inpainting',
        json = {
            'version': 'v2.0',
            'image': image,
            'mask': mask
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    response = json.loads(r.content)
    return response

# 이미지 파일 불러오기
img = Image.open('image.png')
mask = Image.open('mask.png')

# 이미지를 Base64 인코딩하기
img_base64 = imageToString(img)
mask_base64 = imageToString(mask)

# 이미지 편집하기 REST API 호출
response = inpainting(img_base64, mask_base64)

# 응답의 첫 번째 이미지 생성 결과 출력하기
image_url = response.get("images")[0].get("image")
result = Image.open(urllib.request.urlopen(image_url))
result.show()

# 이미지 파일로 저장하기
result.save("inpainting_image.png")
