# Sensitive Data Exposure

from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# 사용자 데이터베이스 초기화 (비밀번호 해싱 저장)
def init_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,  -- 비밀번호를 해싱된 형태로 저장
            email TEXT
        )
    """)

    # 해싱된 비밀번호로 사용자 정보 저장
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (1, 'Alice', ?, 'alice@example.com')",
                   (generate_password_hash('password123'),))
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (2, 'Bob', ?, 'bob@example.com')",
                   (generate_password_hash('bobspassword'),))
    conn.commit()
    conn.close()

# 로그인 페이지
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 사용자 이름으로 데이터베이스에서 사용자 정보 조회
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # 해싱된 비밀번호 검증
            return redirect(url_for("welcome"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

# 환영 페이지
@app.route("/welcome")
def welcome():
    return "<h1>Welcome to the secure area!</h1>"

if __name__ == "__main__":
    init_db()
    # SSL 인증서를 지정하여 HTTPS로 Flask 앱 실행
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443)
