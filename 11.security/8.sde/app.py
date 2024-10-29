# Sensitive Data Exposure
# 설명: 암호화되지 않은 민감한 데이터가 전송되거나 저장되어 공격자가 이를 탈취할 수 있는 취약점입니다.
# 예시: 비밀번호를 평문으로 저장하거나, HTTP로 전송하여 데이터가 암호화되지 않은 상태로 노출됩니다.
# 해결 방법: HTTPS를 사용해 데이터 전송을 암호화하고, 비밀번호는 해시화하여 저장합니다.

from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# 사용자 데이터베이스 초기화 (비밀번호 평문 저장)
def init_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,  -- 비밀번호 평문 저장
            email TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (1, 'Alice', 'password123', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (2, 'Bob', 'bobspassword', 'bob@example.com')")
    conn.commit()
    conn.close()

# 로그인 페이지
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 평문 비밀번호로 데이터베이스 쿼리
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
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
    app.run(debug=True)  # HTTP로 실행
