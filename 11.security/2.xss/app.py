# XSS (Cross-Site Scripting)
# 설명: 사용자가 입력한 데이터가 HTML로 렌더링되어 악성 스크립트가 실행될 수 있는 취약점입니다.
# 예시: 게시판이나 댓글란에 <script>alert('XSS')</script>를 삽입하여 다른 사용자가 페이지를 방문할 때 악성 스크립트가 실행됩니다.
# 해결 방법: 모든 사용자 입력을 HTML로 출력하기 전에 이스케이프 처리하거나, HTML을 필터링하여 스크립트가 실행되지 않도록 합니다.

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# 메시지를 저장할 리스트
message_list = []

@app.route("/", methods=["GET"])
def index():
    # static 폴더의 index.html 파일을 직접 서빙
    return send_file("static/index.html")

@app.route("/messages", methods=["GET", "POST", "DELETE"])
def messages():
    if request.method == "POST":
        # 메시지를 받아 리스트에 추가
        user_input = request.json.get("user_input")
        message = f"Hello, {user_input}!"  # XSS 취약점 발생 지점
        message_list.append(message)
        return jsonify({"messages": message_list})
    
    elif request.method == "DELETE":
        # 메시지 리스트를 초기화
        message_list.clear()
        return jsonify({"messages": message_list})

    # 메시지 리스트 반환
    return jsonify({"messages": message_list})

if __name__ == "__main__":
    app.run(debug=True)
