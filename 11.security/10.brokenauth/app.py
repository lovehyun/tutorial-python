# Broken Authentication and Session Management
# 설명: 세션 토큰이 안전하게 저장되지 않거나, 세션 타임아웃이 설정되지 않아 공격자가 세션을 탈취하여 불법적으로 접근할 수 있는 취약점입니다.
# 예시: 세션 토큰이 암호화되지 않고 브라우저에 저장되거나, 세션 만료 시간이 설정되지 않아 공격자가 세션 탈취 후 계속 액세스할 수 있습니다.
# 해결 방법: 세션에 만료 시간을 설정하고, 세션 토큰을 암호화하여 안전하게 저장합니다.

# 아래 예제에서는 세션 타임아웃을 설정하지 않아 세션이 지속되는 상태로 사용자가 애플리케이션을 종료해도 다른 사람이 같은 세션으로 접근할 수 있도록 합니다.

from flask import Flask, request, render_template, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 단순히 암호화된 키 설정
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)  # 세션 만료 시간 5분 설정

# 사용자 데이터베이스 시뮬레이션
users = {'Alice': {'password': 'password123'}}

# 로그인 페이지
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 사용자 인증
        if username in users and users[username]['password'] == password:
            session['username'] = username  # 세션에 사용자 이름 저장
            return redirect(url_for("profile"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

# 사용자 프로필 페이지
@app.route("/profile")
def profile():
    # 세션이 만료되지 않아서 항상 접근 가능
    if 'username' not in session:
        return redirect(url_for("login"))
    return f"<h1>Welcome, {session['username']}!</h1><a href='/logout'>Logout</a>"

# 로그아웃 기능
@app.route("/logout")
def logout():
    session.pop('username', None)  # 세션에서 사용자 정보 제거
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
