import os

from dotenv import load_dotenv
from google import genai

# .env 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv("GEMINI_API_KEY")

# 클라이언트 생성
client = genai.Client(
    api_key=API_KEY
)

# Gemini 요청
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="파이썬을 쉽게 설명해줘"
)

# 출력
print(response.text)
