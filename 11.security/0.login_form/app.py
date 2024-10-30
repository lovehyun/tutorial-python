from flask import Flask, request, jsonify

app = Flask(__name__)

# 간단한 사용자 정보 로컬 변수로 설정
users = [
    {"username": "admin", "password": "admin123"}
]

@app.route("/", methods=["GET"])
def login_form():
    # 직접 접근 가능한 static 폴더의 HTML 파일 경로를 반환
    return app.send_static_file("login.html")

@app.route("/login", methods=["POST"])
def login():
    # form data에서 username과 password를 가져옴
    username = request.form.get("username")
    password = request.form.get("password")

    print(f"Username: {username}, Password: {password}")

    # for loop로 users 리스트 순회하여 일치하는 사용자인지 확인
    for user in users:
        if user["username"] == username and user["password"] == password:
            return "Login successful", 200
        
    return "Login Failed", 401

@app.route("/welcome")
def welcome():
    return "<h1>Welcome to the secure area!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
