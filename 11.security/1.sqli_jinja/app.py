from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# 간단한 사용자 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # SQL Injection에 취약한 쿼리
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        # FIXME: 위의 쿼리는 사용자가 입력한 값이 직접 쿼리에 포함됩니다.
        # 예를 들어, username에 'admin' -- 을 입력하면 password 부분이 무시되고,
        # SELECT * FROM users WHERE username = 'admin' -- AND password = '...' 가 되어
        # 비밀번호 없이 로그인할 수 있습니다.

        # TODO: 파라미터 바인딩을 통해 SQL Injection 방지
        # query = "SELECT * FROM users WHERE username = ? AND password = ?"

        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute(query)  # SQL Injection 취약성이 있는 코드 실행

        # TODO: 안전한 쿼리 실행
        # cursor.execute(query, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template("welcome.html")
        else:
            error = "Invalid credentials. Please try again."

    return render_template("login.html", error=error)

@app.route("/welcome")
def welcome():
    return "<h1>Welcome to the secure area!</h1>"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
