from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')
# SocketIO(app): Flask 애플리케이션 app을 SocketIO와 연결합니다. 이렇게 하면 Flask 애플리케이션에서 WebSocket 프로토콜을 사용할 수 있게 됩니다.
# async_mode='threading': Flask-SocketIO가 비동기 작업을 처리하는 방식을 지정합니다. 여기서 threading 모드는 Python의 표준 스레딩 라이브러리를 사용하여 비동기 이벤트를 처리합니다.

thread = None
stop_thread = False

def send_numbers():
    # 백그라운드 스레드에서 실행되는 함수로, 1초마다 증가하는 숫자를 웹소켓을 통해 클라이언트로 전송합니다.
    global stop_thread
    number = 1
    
    print("'send_numbers' thread is just about to start... ")

    while not stop_thread:
        print(f"sending message 'number: {number}'")
        socketio.emit('number', {'number': number}, namespace='/')
        number += 1
        time.sleep(1)

    print("'send_numbers' thread is just about to be terminated... ")

@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('start')
def handle_start():
    # 클라이언트에서 'start' 이벤트를 수신했을 때 호출되는 함수로, 백그라운드 스레드를 시작합니다.
    global thread, stop_thread

    print("'start' message received")

    if thread is None or not thread.is_alive():
        stop_thread = False
        thread = threading.Thread(target=send_numbers)
        thread.start()

@socketio.on('stop')
def handle_stop():
    # 클라이언트에서 'stop' 이벤트를 수신했을 때 호출되는 함수로, 백그라운드 스레드를 중지합니다.
    global stop_thread

    print("'stop' message received")

    stop_thread = True

if __name__ == '__main__':
    socketio.run(app, debug=True)
