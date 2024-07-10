# pip install python-dotenv
import requests
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

openai_api_key = os.getenv('OPENAI_API_KEY')

def get_chat_gpt_response(user_input):
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': user_input},
                ],
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {openai_api_key}',
            }
        )

        response.raise_for_status()  # Raise an error for bad HTTP status codes
        response_data = response.json()
        print('-'*20)
        print('Response JSON:', response_data)  # Print the entire response for debugging
        print('-'*20)

        return response.json()['choices'][0]['message']['content']
    except Exception as error:
        print('ChatGPT API 요청 중 오류 발생:', str(error))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'

def chat_with_user():
    user_input = '안녕, 챗봇!'
    chat_gpt_response = get_chat_gpt_response(user_input)
    print('챗봇 응답:', chat_gpt_response)

# 챗봇과 대화 시작
chat_with_user()

# 2초 간격으로 요청 보내기
# while True:
#     chat_with_user()
#     sleep(2)
