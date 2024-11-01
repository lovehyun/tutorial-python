# Insecure Direct Object References (IDOR)
# 설명: 인증된 사용자가 URL 파라미터나 요청 경로를 통해 다른 사용자의 데이터에 직접 접근할 수 있는 취약점입니다.
# 예시: /user_profile?user_id=1처럼 URL에 파라미터로 사용자 ID를 전달하면, ID 값을 변경하여 다른 사용자의 정보를 조회할 수 있습니다.
# 해결 방법: 모든 민감한 데이터 접근에 대한 권한 검증을 추가합니다.

from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션에 사용될 비밀 키 설정

# 사용자 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT, bio TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email, bio) VALUES (1, 'Alice', 'password123', 'alice@example.com', 'Loves hiking')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email, bio) VALUES (2, 'Bob', 'password123', 'bob@example.com', 'Enjoys painting')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email, bio) VALUES (3, 'Charlie', 'password123', 'charlie@example.com', 'Fan of music')")
    conn.commit()
    conn.close()

# 로그인 페이지
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for("user_profile", user_id=user[0]))  # 로그인 후 리디렉션
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

# IDOR가 가능한 사용자 프로필 페이지
@app.route("/user_profile")
def user_profile():
    # URL 파라미터에서 user_id를 직접 가져옴
    user_id = request.args.get("user_id")

    # 주의: 현재는 세션 검사 없이 URL 파라미터의 user_id를 그대로 사용
    user = get_user_by_id(user_id)
    if user:
        return render_template("profile.html", user=user)
    else:
        return "User not found", 404

# 사용자 정보를 ID로 조회
def get_user_by_id(user_id):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# 프로필 수정 페이지
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    # URL 파라미터로 user_id를 직접 받아서 다른 사용자의 정보를 수정할 수 있는 취약점 발생
    user_id = request.args.get("user_id")

    if request.method == "POST":
        email = request.form.get("email")
        bio = request.form.get("bio")

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ?, bio = ? WHERE id = ?", (email, bio, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for("user_profile", user_id=user_id))

    user = get_user_by_id(user_id)
    if user:
        return render_template("edit_profile.html", user=user)
    else:
        return "User not found", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
