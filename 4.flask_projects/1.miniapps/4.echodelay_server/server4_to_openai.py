from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    message = data.get('message', '')
    task_id = data.get('taskId', 'unknown')

    print(f'[F1] 받은 메시지: {message} (작업 ID: {task_id})')

    print(f'[F2] OpenAI에 요청 중...')
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        response_message = response.choices[0].message.content.strip()
        print(f'[F3] OpenAI 응답 완료 (ID: {task_id}): {response_message}')
        return jsonify({ 'response': response_message })

    except Exception as e:
        print(f'[F3] OpenAI 요청 실패:', e)
        return jsonify({ 'response': f'[오류] OpenAI 요청 실패: {str(e)}' }), 500

if __name__ == '__main__':
    print('🟢 Flask 서버 실행 중: http://localhost:5000')
    app.run(port=5000)
