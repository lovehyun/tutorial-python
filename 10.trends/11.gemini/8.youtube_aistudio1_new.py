# pip install google-genai python-dotenv

import csv
import os

from dotenv import load_dotenv
from google import genai

# -----------------------------------
# .env 로드
# -----------------------------------

load_dotenv()

# API 키 가져오기
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

videos = []

with open("video_stats.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        videos.append({
            "title": row["title"],
            "views": row["view_count"],
            "likes": row["like_count"],
            "comments": row["comment_count"]
        })

# -----------------------------------
# 프롬프트 생성
# -----------------------------------

prompt = f"""
다음 유튜브 영상 데이터를 분석해서:

1. 어떤 영상이 가장 인기있는지
2. 인기있는 이유가 무엇인지
3. 어떤 주제가 반응이 좋은지
4. 유튜브 채널 운영 전략

을 자세하게 분석해줘.

영상 데이터:
{videos}
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
