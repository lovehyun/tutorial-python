from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import datetime
import random

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

# 정적 파일 서빙 설정: 캐시를 사용하지 않도록 설정
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 기본 경로('/') 요청 처리: index2.html을 반환
@app.route('/')
def index():
    return app.send_static_file('index2.html')

# 정적 파일 요청 처리: static 폴더에서 파일을 반환
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# 단어 목록
words = ["apple", "banana", "cat", "dog", "fish", "house", "sun", "tree", "water", "bird"]
current_word = ""
drawer = None

# 현재 시간을 문자열로 반환하는 함수
def current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 클라이언트가 소켓에 연결될 때 호출되는 이벤트 핸들러
@socketio.on('connect')
def handle_connect():
    global drawer
    print(f'[{current_time()}] User connected: {request.sid}')
    
    # drawer가 설정되지 않았다면, 현재 사용자를 drawer로 설정하고 새로운 단어를 선택하여 drawer에게 알림
    if not drawer:
        drawer = request.sid
        select_new_word_and_notify_drawer()
    else:
        # 이미 drawer가 존재하므로, 새로 접속한 클라이언트에게 drawer 정보를 보냄
        emit('drawerSelected', drawer)

# 그림 그리기 시작 이벤트 핸들러
@socketio.on('startDrawing')
def handle_start_drawing(data):
    print(f'Start drawing at: ({data["x"]}, {data["y"]})')
    emit('startDrawing', data, broadcast=True)

# 그림 그리기 이벤트 핸들러
@socketio.on('drawing')
def handle_drawing(data):
    emit('drawing', data, broadcast=True)

# 정답 추측 이벤트 핸들러
@socketio.on('guess')
def handle_guess(guess):
    global drawer, current_word
    sanitized_guess = guess.replace('\n', '').replace('\r', '')
    print(f'[{current_time()}] User {request.sid} guessed: {sanitized_guess}')
    emit('guess', {'player': request.sid, 'guess': sanitized_guess}, broadcast=True)
    
    # 추측이 정답과 일치하면, drawer를 해당 사용자로 변경하고 새로운 단어 선택하여 drawer에게 알림
    if sanitized_guess.lower() == current_word.lower():
        emit('correctGuess', request.sid, broadcast=True)
        drawer = request.sid
        select_new_word_and_notify_drawer()

# 캔버스 초기화 이벤트 핸들러
@socketio.on('clearCanvas')
def handle_clear_canvas():
    emit('clearCanvas', broadcast=True)

# 연결이 종료될 때 호출되는 이벤트 핸들러
@socketio.on('disconnect')
def handle_disconnect():
    global drawer
    print(f'[{current_time()}] User disconnected: {request.sid}')
    
    # 연결이 종료된 사용자가 drawer였다면, 다른 클라이언트들 중에서 새로운 drawer를 선택하여 drawer에게 알림
    if request.sid == drawer:
        clients = [client for client in socketio.server.manager.get_participants('/', '/')]
        if clients:
            drawer = clients[0]
            select_new_word_and_notify_drawer()
        else:
            drawer = None

# 새로운 단어를 선택하고 drawer에게 알리는 함수
def select_new_word_and_notify_drawer():
    global current_word, drawer
    current_word = random.choice(words)
    emit('drawerSelected', drawer, broadcast=True)
    socketio.emit('newWord', current_word, room=drawer)
    print(f'[{current_time()}] New turn: {drawer} is drawing {current_word}')

# 메인 실행 부분
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
