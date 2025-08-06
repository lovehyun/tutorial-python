# pip install python-dotenv
import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

openai_api_key = os.getenv('OPENAI_API_KEY')

def ask_chatgpt(user_input):
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            json={
                'model': 'gpt-3.5-turbo', # 'gpt-4'
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': user_input},
                ],
                # "temperature": 0.7,       # 높을수록 창의적, 낮을수록 결정적 응답 (기본값: 1.0, 범위: 0.0~2.0)
                # "top_p": 0.9,             # 확률 기반 샘플링, 낮을수록 보수적 (0.9는 상위 90% 만 사용) (기본값: 1.0, 범위: 0.0~1.0)
                # "max_tokens": 150,        # 응답의 최대 길이
                # "frequency_penalty": 0.5, # 높을수록 같은 단어 반복 방지 (기본값: 0.0, 범위: -2.0~2.0)
                # "presence_penalty": 0.3   # 높을수록 새로운 주제 등장 가능성 증가 (기본값: 0.0, 범위: -2.0~2.0)
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


# 챗봇과 대화 시작
print('챗봇 응답:', ask_chatgpt('안녕, 챗봇!'))
print('챗봇 응답:', ask_chatgpt('너는 뭘 해줄수 있니?'))
