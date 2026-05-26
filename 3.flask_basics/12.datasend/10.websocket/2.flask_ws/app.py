# pip install flask flask-sock

from flask import Flask
from flask import send_from_directory
from flask_sock import Sock

app = Flask(__name__, static_folder="static")
sock = Sock(app)

# -----------------------------
# HTML 페이지 서빙
# -----------------------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# -----------------------------
# WebSocket 서버
# ws://localhost:5000/ws
# -----------------------------
@sock.route("/ws")
def websocket(ws):

    print("클라이언트 연결됨!")

    # 최초 연결 메시지
    ws.send("서버에 연결되었습니다!")

    while True:
        try:
            # 클라이언트 메시지 수신
            message = ws.receive()

            if message is None:
                break

            print("클라이언트 메시지:", message)

            # 다시 클라이언트로 응답
            ws.send(f"서버가 받은 메시지: {message}")

        except Exception as e:
            print("에러 발생:", e)
            break

    print("클라이언트 연결 종료")


if __name__ == "__main__":
    app.run(debug=True)
