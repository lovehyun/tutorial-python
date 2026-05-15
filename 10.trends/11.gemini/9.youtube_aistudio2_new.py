# pip install google-genai python-dotenv

import csv
import os

from dotenv import load_dotenv
from google import genai

# -----------------------------------
# .env 로드
# -----------------------------------

load_dotenv()

# Gemini API 키 가져오기
API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------------
# Gemini Client 생성
# -----------------------------------

client = genai.Client(
    api_key=API_KEY
)

# -----------------------------------
# CSV 읽기
# -----------------------------------

titles = []

with open("video_stats.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        titles.append(row["title"])

# -----------------------------------
# 프롬프트 생성
# -----------------------------------

prompt = f"""
다음 유튜브 영상 제목들을 참고해서:

1. 클릭률이 높을 것 같은 제목 패턴 분석
2. 사람들이 좋아할 제목 스타일 분석
3. 비슷한 스타일의 새로운 제목 10개 생성

해줘.

기존 제목:
{titles}
"""

# -----------------------------------
# Gemini 요청
# -----------------------------------

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# -----------------------------------
# 결과 출력
# -----------------------------------

print(response.text)
