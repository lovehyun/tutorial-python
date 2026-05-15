# pip install google-genai python-dotenv

import os

from dotenv import load_dotenv
from google import genai

# -----------------------------------
# .env 로드
# -----------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------------
# Gemini Client 생성
# -----------------------------------

client = genai.Client(
    api_key=API_KEY
)

# -----------------------------------
# 메모리(history) 저장소
# -----------------------------------

memory = []

# -----------------------------------
# 채팅 함수
# -----------------------------------

def chat(user_message):

    # 사용자 메시지 저장
    memory.append(f"사용자: {user_message}")

    # 전체 history 합치기
    prompt = "\n".join(memory)

    # Gemini 요청
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    ai_message = response.text

    # AI 응답도 memory 저장
    memory.append(f"AI: {ai_message}")

    return ai_message

# -----------------------------------
# 대화 테스트
# -----------------------------------

print(chat("내 이름은 홍길동이야"))

print("=" * 50)

print(chat("내가 좋아하는 언어는 파이썬이야"))

print("=" * 50)

print(chat("내 이름이 뭐야?"))

print("=" * 50)

print(chat("내가 좋아하는 언어는 뭐야?"))
