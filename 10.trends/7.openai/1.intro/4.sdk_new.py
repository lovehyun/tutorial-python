# pip install openai==1.0
# https://platform.openai.com/docs/api-reference/introduction

import openai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

openai_api_key = os.getenv('OPENAI_API_KEY')

def get_chat_gpt_response(user_input):
    try:
        # Create a client instance
        client = openai.OpenAI(api_key=openai_api_key)

        # Use the updated method for chat completions
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': user_input},
            ],
            # temperature=0.7,        # 창의성 조절 (0.0 ~ 2.0)
            # top_p=0.9,              # 확률 기반 샘플링 (0.0 ~ 1.0)
            # max_tokens=150,         # 응답 최대 길이
            # frequency_penalty=0.5,  # 반복 단어 방지 (-2.0 ~ 2.0)
            # presence_penalty=0.3    # 새로운 주제 등장 가능성 증가 (-2.0 ~ 2.0)
        )
        print('-'*20)
        print('Response JSON:', response)  # Print the entire response for debugging
        print('-'*20)

        return response.choices[0].message.content
    except Exception as error:
        print('ChatGPT API 요청 중 오류 발생:', str(error))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'

def chat_with_user():
    # user_input = '안녕, 챗봇!'
    user_input = input('사용자 입력: ')
    chat_gpt_response = get_chat_gpt_response(user_input)
    print('챗봇 응답:', chat_gpt_response)

# 챗봇과 대화 시작
chat_with_user()
