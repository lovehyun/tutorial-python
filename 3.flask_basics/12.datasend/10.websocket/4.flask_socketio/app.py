# pip install flask flask-socketio
# WebSocket = 저수준 통신 기술
# Socket.IO = 그 위를 편하게 감싼 라이브러리
#   - 연결 끊김 처리
#   - 재연결
#   - 이벤트 이름 관리
#   - 브로드캐스트
#   - room/group 관리
#   - fallback 처리

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, send

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory("static", "index.html")

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
