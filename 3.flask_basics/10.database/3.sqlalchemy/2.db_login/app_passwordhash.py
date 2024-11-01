# pip install flask-sqlalchemy
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))
    email = db.Column(db.String(100))

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        found_user = User.query.filter_by(name=username).first()
        if found_user and check_password_hash(found_user.password, password):
            session["user"] = username
            session["email"] = found_user.email
            flash("Login Successful!")
            return redirect(url_for("user"))
        else:
            flash("Invalid username or password, please try again.")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            
            found_user = User.query.filter_by(username=user).first()
            found_user.email = email
            db.session.commit()
            
            flash("Email was saved!")
        else:
            email = session.get("email")
                
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # 기본 사용자 추가 (필요한 경우)
        if not User.query.filter_by(name="user1").first():
            user1 = User(username="user1", password="password1", email="user1@example.com")
            user2 = User(username="user2", password="password2", email="user2@example.com")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    app.run(debug=True, port=5000)
