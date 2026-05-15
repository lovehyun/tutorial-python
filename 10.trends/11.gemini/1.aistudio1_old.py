# pip install google-generativeai

# https://aistudio.google.com/api-keys
# OpenAI 등 처럼 크레딧 주는 개념 아니고 프리티어
# 대략 15 RPM (분당 15 요청 정도)

import google.generativeai as genai

API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "파이썬이 무엇인지 초등학생 수준으로 설명해줘"
)

print(response.text)
