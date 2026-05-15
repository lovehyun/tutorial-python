from flask import Flask, request, send_from_directory, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='public')
port = int(os.environ.get("PORT", 5000))
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('userInput', '')
    chatgpt_response = get_chatgpt_response(user_input)
    return jsonify({'chatGPTResponse': chatgpt_response})


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


def get_chatgpt_response(user_input):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            #    temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as error:
        print('Error:', str(error))
        return '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
