from dotenv import load_dotenv
import os
import requests

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_chat_gpt_response(user_input):
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        json={
            'model': 'gpt-3.5-turbo', # gpt-4o-mini 
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                # {'role': 'system', 'content': 'You are a cook who can make delicious korean food.'},
                {'role': 'user', 'content': user_input}
            ],
        },
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
    )

    response_data = response.json()
    return response_data['choices'][0]['message']['content']
    
user_input = "안녕하세요"
print("챗봇 응답: ", get_chat_gpt_response(user_input))
