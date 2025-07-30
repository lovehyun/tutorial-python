from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)

# 보안 키 및 세션 설정
app.config['SECRET_KEY'] = 'abcd1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# 테스트 사용자
users = [
    {'name': 'MyName', 'id': 'user', 'pw': 'password'},
]

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("user"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        input_id = request.form.get("id")
        input_pw = request.form.get("pw")

        user = next((u for u in users if u["id"] == input_id and u["pw"] == input_pw), None)
        if user:
            session.permanent = True
            session["user"] = user
            flash("로그인에 성공했습니다!", "success")
            return redirect(url_for("user"))
        else:
            flash("아이디 또는 비밀번호가 틀렸습니다.", "danger")
            return redirect(url_for("login"))

    if "user" in session:
        flash("이미 로그인된 사용자입니다.", "info")
        return redirect(url_for("user"))

    return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        return render_template("user.html", user=session["user"])
    else:
        flash("로그인이 필요합니다.", "warning")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        flash("정상적으로 로그아웃 되었습니다.", "info")
        session.pop("user", None)
    else:
        flash("이미 로그아웃된 상태입니다.", "warning")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
