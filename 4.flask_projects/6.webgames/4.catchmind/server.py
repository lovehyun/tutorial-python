# pip install flask_socketio

from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import datetime
import random

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

# 기존의 정적 파일 서빙 부분을 수정합니다.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 기본 파일을 index2.html로 설정합니다.
@app.route('/')
def index():
    return app.send_static_file('index2.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

words = ["apple", "banana", "cat", "dog"]
current_word = ""
drawer = None

def current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@socketio.on('connect')
def handle_connect():
    global drawer
    print(f'[{current_time()}] User connected: {request.sid}')
    
    if not drawer:
        drawer = request.sid
        select_new_word_and_notify_drawer()

@socketio.on('startDrawing')
def handle_start_drawing(data):
    print(f'Start drawing at: ({data["x"]}, {data["y"]})')
    emit('startDrawing', data, broadcast=True)

@socketio.on('drawing')
def handle_drawing(data):
    emit('drawing', data, broadcast=True)

@socketio.on('guess')
def handle_guess(guess):
    global drawer, current_word
    sanitized_guess = guess.replace('\n', '').replace('\r', '')
    print(f'[{current_time()}] User {request.sid} guessed: {sanitized_guess}')
    emit('guess', {'player': request.sid, 'guess': sanitized_guess}, broadcast=True)
    if sanitized_guess == current_word:
        emit('correctGuess', request.sid, broadcast=True)
        drawer = request.sid
        select_new_word_and_notify_drawer()

@socketio.on('clearCanvas')
def handle_clear_canvas():
    emit('clearCanvas', broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global drawer
    print(f'[{current_time()}] User disconnected: {request.sid}')
    if request.sid == drawer:
        clients = [client for client in socketio.server.manager.get_participants('/', '/')]
        if clients:
            drawer = clients[0]
            select_new_word_and_notify_drawer()
        else:
            drawer = None

def select_new_word_and_notify_drawer():
    global current_word, drawer
    current_word = random.choice(words)
    emit('drawerSelected', drawer, broadcast=True)
    socketio.emit('newWord', current_word, room=drawer)
    print(f'[{current_time()}] New turn: {drawer} is drawing {current_word}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
