# curl -X GET http://127.0.0.1:5000/set-session/user1234 -c cookies.txt
# curl -X GET http://127.0.0.1:5000/set-session/user1234 --cookie-jar cookies.txt
# curl -X GET http://127.0.0.1:5000/get-session -b cookies.txt
# curl -X GET http://127.0.0.1:5000/get-session --cookie cookies.txt

from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 암호화를 위한 키 설정

# eyJ1c2VybmFtZSI6InRlc3RfdXNlciJ9.YX_x2Q.lVpJb0hKsWlGgS4F_XCkQg2MjcQ
# eyJ1c2VybmFtZSI6InRlc3RfdXNlciJ9 → Base64로 인코딩된 JSON 데이터 (username: test_user)
# YX_x2Q → 만료 시간 (있을 경우)
# lVpJb0hKsWlGgS4F_XCkQg2MjcQ → HMAC 서명 (데이터 변조 방지)
# JSON.parse(atob(base64data)) # → {'username':'test_user'}
# btoa(string) # 반대로 JSON을 인코딩문자열로

# 이 모든 걸 Flask가 자동으로 처리해주며, 서버에는 세션 데이터가 저장되지 않습니다.
# 클라이언트가 모든 세션 데이터를 쿠키에 담아야 함 (용량 제한 있음: 보통 4KB)
# 민감한 정보 저장 부적합

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
