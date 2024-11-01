from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

# 사용자 데이터 저장하는 리스트
users = [
    {"id": 1, "username": "user1", "password": "password1"},
    {"id": 2, "username": "user2", "password": "password2"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        # 사용자 데이터 리스트에서 사용자 정보 찾기
        user_data = next((user for user in users if user["username"] == username), None)

        if user_data and user_data["password"] == password:
            session["user"] = username
            flash("Login Successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for("login"))

    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    flash("You have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
