# 취약한 코드 입력
# <script>alert('XSS Attack!');</script>

from flask import Flask, request, render_template

app = Flask(__name__)

# 메시지를 저장할 리스트
message_list = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 사용자 입력을 받아 리스트에 추가
        user_input = request.form.get("user_input")
        message = f"Hello, {user_input}!"  # XSS 취약점 발생 지점
        message_list.append(message)  # 메시지를 리스트에 추가
    
    # 템플릿 렌더링
    return render_template("index.html", messages=message_list)

if __name__ == "__main__":
    app.run(debug=True)
