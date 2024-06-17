from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        password = request.form["password"]

        found_user = User.query.filter_by(username=user).first()
        if found_user and found_user.password == password:
            session["user"] = user
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
    with app.app_context():
        db.create_all()
        # 기본 사용자 추가 (필요한 경우)
        if not User.query.first():
            user1 = User(username="user1", password="password1")
            user2 = User(username="user2", password="password2")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        # 데이터 조회
        users = User.query.all()
        print('-' * 30)
        for user in users:
            print(user.id, user.username, user.password)  # SQLAlchemy 객체의 속성을 사용하여 값에 접근
        print('-' * 30)

    app.run(debug=True, port=5000)
