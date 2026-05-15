# 예제 2. "조회수 잘 나올 제목 추천"
import csv
import os

from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------------
# .env 로드
# -----------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini 설정
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------------
# CSV 읽기
# -----------------------------------

titles = []

with open("video_stats.csv", "r", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        titles.append(row["title"])

# -----------------------------------
# 프롬프트
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

response = model.generate_content(prompt)

print(response.text)
