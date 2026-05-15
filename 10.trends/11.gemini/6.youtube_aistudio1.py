# pip install google-generativeai python-dotenv   <-- 구버전
# pip install google-genai  <-- 신버전

# 예제 1. "어떤 영상이 인기인지 분석"
import csv
import os

from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------------
# .env 로드
# -----------------------------------

load_dotenv()

# Gemini API 키
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini 설정
genai.configure(api_key=API_KEY)

# 모델 생성
model = genai.GenerativeModel("gemini-2.5-flash")

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
# Gemini 프롬프트 생성
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

response = model.generate_content(prompt)

# 결과 출력
print(response.text)
