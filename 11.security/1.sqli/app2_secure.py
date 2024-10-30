# SQL Injection
# 설명: 사용자가 입력한 데이터가 SQL 쿼리에 직접 포함되어, 공격자가 쿼리를 조작하여 데이터베이스를 부당하게 읽거나 수정할 수 있는 취약점입니다.
# 예시: 로그인 폼에서 username에 ' OR '1'='1과 같은 입력값을 주면 비밀번호 없이 인증이 우회됩니다.
# 해결 방법: Prepared Statements 및 ORM을 사용하여 사용자 입력이 쿼리로 직접 전달되지 않도록 합니다.

from flask import Flask, request, jsonify
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

@app.route("/", methods=["GET"])
def login_form():
    # 직접 접근 가능한 static 폴더의 HTML 파일 경로를 반환
    return app.send_static_file("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # SQL Injection에 취약한 쿼리
    # query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    # FIXME: 위의 쿼리는 사용자가 입력한 값이 직접 쿼리에 포함됩니다.
    # 예를 들어, username에 'admin' -- 을 입력하면 password 부분이 무시되고,
    # SELECT * FROM users WHERE username = 'admin' -- AND password = '...' 가 되어
    # 비밀번호 없이 로그인할 수 있습니다.

    # TODO: 파라미터 바인딩을 통해 SQL Injection 방지
    query = "SELECT * FROM users WHERE username = ? AND password = ?"

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # cursor.execute(query)  # SQL Injection 취약성이 있는 코드 실행

    # TODO: 안전한 쿼리 실행
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    print(user)
    conn.close()
    
    if user:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials. Please try again."})

@app.route("/welcome")
def welcome():
    return "<h1>Welcome to the secure area!</h1>"

if __name__ == "__main__":
    # init_db()
    app.run(debug=True)
