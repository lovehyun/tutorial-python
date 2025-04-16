from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    message = data.get('message', '')
    task_id = data.get('taskId', 'unknown')

    print(f'[F1] 받은 메시지: {message} (작업 ID: {task_id})')

    delay = random.uniform(5, 10)
    # delay = random.uniform(10, 20)
    print(f'[F2] {delay:.2f}초 지연 중...')
    time.sleep(delay)

    response_message = f'Flask 처리 결과: "{message}"에 대한 응답입니다.'
    print(f'[F3] 응답 준비 완료 (ID: {task_id}):', response_message)

    return jsonify({ 'response': response_message })

if __name__ == '__main__':
    print('🟢 Flask 서버 실행 중: http://localhost:5000')
    app.run(port=5000)
