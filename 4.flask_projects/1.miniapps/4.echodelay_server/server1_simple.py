from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    message = data.get('message', '')

    print('[F1] Express로부터 받은 메시지:', message)

    print('[F2] 1초 지연중...')
    time.sleep(1)  # 1초 지연

    response_message = f'Flask에서 받은 메시지: {message}'

    print('[F3] 처리된 메시지 (응답 예정):', response_message)

    return jsonify({ 'response': response_message })

if __name__ == '__main__':
    print('🟢 Flask 서버 실행 중: http://localhost:5000')
    app.run(port=5000)
