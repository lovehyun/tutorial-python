# curl -X GET http://127.0.0.1:5000/set-session/user1234 -c cookies.txt
# curl -X GET http://127.0.0.1:5000/get-session -b cookies.txt

from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 암호화를 위한 키 설정

# 세션 값 설정하기
@app.route("/set-session/<username>")
def set_session(username):
    session['username'] = username  # 세션에 값 저장
    return "Session has been set!"

# 세션 값 가져오기
@app.route("/get-session")
def get_session():
    if 'username' in session:
        return f"Session value: {session['username']}"
    else:
        return "No session value found!"

# 세션 값 삭제하기
@app.route("/clear-session")
def clear_session():
    session.pop('username', None)  # 세션에서 값 삭제
    return "Session has been cleared!"

if __name__ == "__main__":
    app.run(debug=True)
