# CSRF (Cross-Site Request Forgery)
# 설명: 사용자가 의도하지 않은 요청을 악성 사이트에서 보내게 하여, 사용자의 인증된 세션을 악용하는 공격입니다.
# 예시: 사용자가 로그인된 상태에서 공격자가 만든 사이트를 방문하면 사용자의 의지와 상관없이 특정 요청(예: 비밀번호 변경)이 서버로 전송됩니다.
# 해결 방법: CSRF 토큰을 사용하여 사용자가 직접 보낸 요청만 유효하도록 합니다.

from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 간단한 사용자 데이터베이스 시뮬레이션
users = {'Alice': {'password': 'password123'}}

# 로그인 페이지
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 사용자 인증
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for("profile"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

# 사용자 프로필 페이지
@app.route("/profile")
def profile():
    if 'username' not in session:
        return redirect(url_for("login"))

    return render_template("profile.html", username=session['username'])

# 비밀번호 변경 페이지 (CSRF 방지 없음)
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if 'username' not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        new_password = request.form.get("new_password")
        username = session['username']

        # CSRF 방지가 없으므로, 외부 사이트에서 사용자가 원하지 않는 요청을 보내게 할 수 있음
        users[username]['password'] = new_password
        return f"Password for {username} has been changed successfully."

    return render_template("change_password.html")

# 로그아웃 기능
@app.route("/logout")
def logout():
    session.pop('username', None)  # 세션에서 사용자 정보 제거
    return redirect(url_for("login"))  # 로그인 페이지로 리디렉션

if __name__ == "__main__":
    app.run(debug=True)
