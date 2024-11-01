from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

DATABASE = 'users.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT)''')
        conn.commit()

        # 기본 계정 추가
        cur.execute("SELECT COUNT(*) as count FROM users")
        count = cur.fetchone()["count"]
        if count == 0:
            cur.execute("INSERT INTO users (username, password, email) VALUES ('user1', 'password1', 'user1@example.com')")
            cur.execute("INSERT INTO users (username, password, email) VALUES ('user2', 'password2', 'user2@example.com')")
            conn.commit()

        conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        # Select user without prepared statement - ' OR 1=1 -- 또는 ' OR 1=1 #
        cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        user_data = cur.fetchone()
        conn.close()

        if user_data:
            session["user"] = username
            session["email"] = user_data["email"]
            flash("Login Successful!")
            return redirect(url_for("user"))
        else:
            flash("Invalid credentials, please try again.")

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
            
            conn = get_db_connection()
            cur = conn.cursor()
            # Update user email without prepared statement
            cur.execute(f"UPDATE users SET email = '{email}' WHERE username = '{user}'")
            conn.commit()
            conn.close()
            
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
                
                # Fetch email from database without prepared statement
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(f"SELECT email FROM users WHERE username = '{user}'")
                user_email = cur.fetchone()
                conn.close()
                
                if user_email:
                    email = user_email['email']

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
    init_db()
    app.run(debug=True, port=5000)
