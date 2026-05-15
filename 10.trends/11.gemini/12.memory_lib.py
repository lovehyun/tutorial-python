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
# Client 생성
# -----------------------------------

client = genai.Client(
    api_key=API_KEY
)

# -----------------------------------
# Chat 생성
# -----------------------------------

chat = client.chats.create(
    model="gemini-2.5-flash"
)

# -----------------------------------
# 첫 번째 메시지
# -----------------------------------

response1 = chat.send_message(
    "내 이름은 홍길동이야"
)

print("첫 번째 응답:")
print(response1.text)

print("=" * 50)

# -----------------------------------
# 두 번째 메시지
# -----------------------------------

response2 = chat.send_message(
    "내 이름이 뭐야?"
)

print("두 번째 응답:")
print(response2.text)
