from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

DATABASE = 'users.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 행을 sqlite3.Row 객체로 반환하도록 설정 
                                    # (Dict 형태로 접근 가능 = row['id'], 설정하지 않으면 튜플 index를 사용하여 row[0] 로 접근)
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
        conn.commit()

        # 기본 계정 추가
        cur.execute("SELECT COUNT(*) as count FROM users")
        count = cur.fetchone()["count"]
        if count == 0:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user1", "password1"))
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user2", "password2"))
            conn.commit()

        # 데이터 조회
        cur.execute('SELECT * FROM users')
        rows = cur.fetchall()

        print('-' * 30)
        for row in rows:
            print(row['id'], row['username'], row['password'])  # 열 이름을 사용(Dict)하여 값에 접근
        print('-' * 30)
            
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
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = cur.fetchone()
        conn.close()

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
    session.pop("user", None) # user 가 없을때 KeyError를 방지하기 위해서 None 을 추가
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
