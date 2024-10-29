# Weak Password Policy
# 설명: 비밀번호 정책이 약하게 설정되어 짧거나 예측 가능한 비밀번호를 허용할 경우, 공격자가 쉽게 비밀번호를 추측할 수 있습니다.
# 예시: 사용자에게 1234와 같은 짧은 비밀번호를 허용하여, brute-force 공격에 쉽게 노출됩니다.
# 해결 방법: 비밀번호 정책을 강화하여 최소 길이, 대소문자, 숫자, 특수문자를 포함하도록 설정합니다.

from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 간단한 사용자 데이터베이스 (약한 비밀번호 정책)
users = {
    'admin': '1234',  # 쉬운 비밀번호로 보호된 사용자
}

@app.route("/")
def index():
    if 'username' in session:
        return f"<h1>Welcome, {session['username']}!</h1><a href='/logout'>Logout</a>"
    return "<h1>Homepage</h1><a href='/login'>Login</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 단순한 비밀번호 검증
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for("index"))
        return "Invalid credentials", 401

    # 템플릿을 사용한 로그인 페이지 렌더링
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
