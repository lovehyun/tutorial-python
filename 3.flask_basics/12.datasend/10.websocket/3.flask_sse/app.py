# pip install flask
# SSE (Server-Sent Events)
#   - HTTP 위에서 동작하는 단방향 푸시 (서버 -> 클라이언트)
#   - text/event-stream MIME 타입 사용
#   - 클라이언트는 EventSource API 로 수신
#   - 자동 재연결 지원 (브라우저 내장 기능)
#   - 양방향이 필요하면 클라이언트 -> 서버는 일반 HTTP(POST) 로 보내야 함

# [A 브라우저] ----\
# [B 브라우저] ----- > subscribers = [q1, q2, q3]
# [C 브라우저] ----/
#
# A가 POST /send
#         ↓
# for q in subscribers:
#     q.put(...)
#         ↓
# A,B,C 모두 수신

from flask import Flask, send_from_directory
from flask import request, Response
from queue import Queue
import time

app = Flask(__name__, static_folder="static")

# 연결된 클라이언트들의 메시지 큐 목록
subscribers = []


# -----------------------------
# HTML 페이지 서빙
# -----------------------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# -----------------------------
# SSE 스트림
# GET http://localhost:5000/stream
# -----------------------------
@app.route("/stream")
def stream():
    print("클라이언트 연결됨!")

    def event_stream():
        # 이 클라이언트 전용 큐 생성 후 구독자 목록에 등록
        q = Queue()
        subscribers.append(q)

        try:
            # 최초 연결 메시지
            yield f"data: 서버에 연결되었습니다!\n\n"

            while True:
                # 큐에 메시지가 들어올 때까지 대기
                message = q.get()
                if message is None:
                    break

                # SSE 포맷: "data: <내용>\n\n"
                yield f"data: {message}\n\n"

        except GeneratorExit:
            print("클라이언트 연결 종료")
        finally:
            if q in subscribers:
                subscribers.remove(q)

    return Response(event_stream(), mimetype="text/event-stream")


# -----------------------------
# 클라이언트 -> 서버 메시지 수신
# POST http://localhost:5000/send
# -----------------------------
@app.route("/send", methods=["POST"])
def send():
    message = request.form.get("message", "")

    print("클라이언트 메시지:", message)

    # 모든 구독자에게 응답 푸시
    for q in subscribers:
        q.put(f"서버가 받은 메시지: {message}")

    return ("", 204) # 204 = No Content


if __name__ == "__main__":
    # SSE 는 클라이언트 연결마다 워커를 점유하므로 threaded=True 권장
    app.run(debug=True, threaded=True)
