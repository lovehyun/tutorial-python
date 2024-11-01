# CSRF 방지를 위해 CSRF 토큰을 추가하여 사용자가 실제로 직접 보낸 요청인지 검증하는 방식으로 보호할 수 있습니다. 
# Flask-WTF 라이브러리를 활용하면 CSRF 토큰을 쉽게 추가할 수 있습니다.

# 1. Flask-WTF 설치: 먼저, Flask-WTF 패키지를 설치합니다.
#   pip install Flask-WTF
# 2. CSRF 보호 활성화: FlaskForm을 사용하여 CSRF 토큰을 폼에 추가합니다. 
#   그리고 CSRF 보호를 위해 Flask-WTF의 CSRFProtect를 활성화합니다.
# 3. 코드 수정: change_password 페이지에 CSRF 보호를 추가하는 방식으로 보완된 코드입니다.

from flask import Flask, request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)

# 간단한 사용자 데이터베이스 시뮬레이션
users = {'Alice': {'password': 'password123'}}

# 비밀번호 변경 폼 (CSRF 보호가 자동으로 추가됨)
class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])

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

# 비밀번호 변경 페이지 (CSRF 방지 추가)
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if 'username' not in session:
        return redirect(url_for("login"))

    form = ChangePasswordForm()
    if form.validate_on_submit():  # POST 요청 및 CSRF 토큰 검증 포함
        new_password = form.new_password.data
        username = session['username']

        users[username]['password'] = new_password
        return f"Password for {username} has been changed successfully."

    return render_template("change3_password.html", form=form)

# 로그아웃 기능
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
