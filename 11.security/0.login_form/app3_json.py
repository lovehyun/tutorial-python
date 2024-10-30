from flask import Flask, request, jsonify, redirect, url_for

app = Flask(__name__)

# 간단한 사용자 정보 로컬 변수로 설정
users = [
    {"username": "admin", "password": "admin123"}
]

@app.route("/", methods=["GET"])
def login_form():
    # 직접 접근 가능한 static 폴더의 HTML 파일 경로를 반환
    return app.send_static_file("login3_json.html")

@app.route("/login", methods=["POST"])
def login():
    # form data에서 username과 password를 가져옴
    # username = request.form.get("username")
    # password = request.form.get("password")

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print(f"Username: {username}, Password: {password}")

    # 로컬 변수 users에서 사용자 인증 확인
    user = next((user for user in users if user["username"] == username and user["password"] == password), None)

    if user:
        return jsonify({"success": True, "message": "Login successful", "username": username})
    else:
        return jsonify({"success": False, "message": "Invalid credentials. Please try again."})

@app.route("/welcome")
def welcome():
    username = request.args.get("username", "Guest")  # URL 파라미터에서 사용자 이름을 가져옴
    return f"<h1>Welcome, {username}!</h1><h2>You are now in the secure area!</h2>"

if __name__ == "__main__":
    app.run(debug=True)
