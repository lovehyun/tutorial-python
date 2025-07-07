# https://pixabay.com/api/docs/

import requests
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API Key 가져오기
API_KEY = os.getenv('PIXABAY_API_KEY')
BASE_URL = 'https://pixabay.com/api/'

# 검색어 입력
query = 'cat'

# API 요청
params = {
    'key': API_KEY,
    'q': query,
    'image_type': 'photo',
    'per_page': 5  # 가져올 이미지 개수
}

response = requests.get(BASE_URL, params=params)

# 응답 처리
if response.status_code == 200:
    data = response.json()
    hits = data.get('hits', [])
    for i, hit in enumerate(hits, 1):
        print(f"{i}번째 이미지 URL: {hit['webformatURL']}")
else:
    print('요청 실패:', response.status_code)
