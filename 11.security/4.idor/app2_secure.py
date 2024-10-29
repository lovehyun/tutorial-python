# IDOR 취약점을 해결하려면, 사용자가 자신의 프로필에만 접근할 수 있도록 세션의 user_id를 활용하여 URL 파라미터로 전달된 user_id를 무시하고, 세션에서 user_id를 가져와 프로필을 조회하거나 수정하도록 코드를 변경해야 합니다.

from flask import Flask, request, render_template, redirect, url_for, session
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
            # 로그인 성공 시 세션에 사용자 ID 저장
            session['user_id'] = user[0]
            return redirect(url_for("user_profile"))  # 로그인 후 리디렉션
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

# IDOR가 가능한 사용자 프로필 페이지
@app.route("/user_profile")
def user_profile():
    # 세션에서 user_id 가져오기
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = get_user_by_id(user_id)
    if user:
        return render_template("profile_secure.html", user=user)
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
    # 세션에서 user_id 가져오기
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        email = request.form.get("email")
        bio = request.form.get("bio")

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ?, bio = ? WHERE id = ?", (email, bio, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for("user_profile"))

    user = get_user_by_id(user_id)
    if user:
        return render_template("edit_profile.html", user=user)
    else:
        return "User not found", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
