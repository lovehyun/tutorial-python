from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5) # 영구 세션의 유지 시간 설정
# app.permanent_session_lifetime = timedelta(days=7)

users = [
    {'name': 'MyName', 'id': 'user', 'pw': 'password'},
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        input_id = request.form["id"] # request.form.get('id')
        input_pw = request.form["password"] # request.form.get('password')

        user = next((u for u in users if u["id"] == input_id and u["pw"] == input_pw), None)
        if user:
            session.permanent = True # 영구 세션으로 설정
            session["user"] = user["name"]  # name만 저장 (또는 필요 시 전체 user 객체 저장)
            return redirect(url_for("user"))
        else:
            return render_template("login.html", error="아이디 또는 비밀번호가 틀렸습니다.")
    else: # GET
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))

@app.route("/product")
def product():
    user = session.get("user", None)

    return render_template("product.html", user=user)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
