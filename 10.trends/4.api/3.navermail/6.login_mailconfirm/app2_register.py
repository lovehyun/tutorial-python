# pip install flask flask-mail python-dotenv
from flask import Flask, request, session, jsonify, send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv
import random
import os

load_dotenv()  # .env 파일에서 환경변수 로드

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 메일 설정
app.config['MAIL_SERVER'] = os.getenv("NAVER_MAILSERVER")
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("NAVER_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("NAVER_PASSWORD")
mail = Mail(app)

# 로컬 사용자 정보 저장용
users = []

# --------------------- 정적 파일 라우팅 ---------------------

# 정적 파일 제공
@app.route("/")
def home_page():
    return send_from_directory("static", "index2.html")

@app.route("/signup")
def serve_signup_page():
    return send_from_directory("static", "signup2.html")

@app.route("/forgot")
def forgot_page():
    return send_from_directory("static", "forgot2.html")

@app.route("/reset")
def reset_password_page():
    if session.get("auth_email_verified") != True:
        return "잘못된 접근입니다.", 403
    return send_from_directory("static", "reset2.html")

# --------------------- 인증 코드 관련 ---------------------

# 인증 코드 발송
@app.route("/send-code", methods=["POST"])
def send_code():
    email = request.json.get("email")
    if not email:
        return jsonify({"error": "이메일을 입력해주세요"}), 400

    code = str(random.randint(100000, 999999))
    session["auth_code"] = code
    session["auth_email"] = email

    msg = Message("회원가입 인증 코드", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"인증 코드: {code}"
    mail.send(msg)
    
    print(f"[DEBUG] 인증코드 발송 대상 이메일: {email}, 코드: {code}")

    return jsonify({"message": "인증 코드가 전송되었습니다"})

# 인증 코드 검증
@app.route("/verify-code", methods=["POST"])
def verify_code():
    input_code = request.json.get("code")
    email = session.get("auth_email")
    stored_code = session.get("auth_code")

    print(f"[DEBUG] 세션에 저장된 인증코드: {stored_code}, 사용자 입력: {input_code}")

    if stored_code == input_code:
        session["auth_email_verified"] = True
        session["auth_email"] = email
        return jsonify({"message": "인증 성공"})
    return jsonify({"error": "인증 실패"}), 400

# --------------------- 로그인/회원가입 ---------------------

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:
            session["user"] = username  # 로그인된 사용자 저장
            return jsonify({"message": f"{username}님 로그인 성공"})
    
    return jsonify({"error": "아이디 또는 비밀번호가 올바르지 않습니다"}), 401

@app.route("/signup-action", methods=["POST"])
def signup_action():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # 주의. 프런트엔드에서 체크한 emailVerified 는 신뢰 할 수 없음!!
    # if not session.get("auth_email_verified") or session.get("auth_email") != email:
        # return jsonify({"error": "이메일 인증이 필요합니다"}), 400

    if any(u['username'] == username for u in users):
        return jsonify({"error": "이미 존재하는 아이디입니다"}), 400

    users.append({
        "username": username,
        "password": password,
        "email": email
    })

    # 인증 관련 세션 제거
    session.pop("auth_code", None)
    session.pop("auth_email", None)
    session.pop("auth_email_verified", None)

    return jsonify({"message": "회원가입 완료"})

# --------------------- 비밀번호 재설정 ---------------------

@app.route("/reset-password", methods=["POST"])
def reset_password():
    email = session.get("auth_email")
    if not session.get("auth_email_verified") or not email:
        return jsonify({"error": "인증된 이메일이 없습니다"}), 403

    new_password = request.json.get("password")
    if not new_password:
        return jsonify({"error": "새 비밀번호를 입력해주세요"}), 400

    for user in users:
        if user["email"] == email:
            user["password"] = new_password
            break
    else:
        return jsonify({"error": "해당 이메일의 사용자를 찾을 수 없습니다"}), 404

    # 인증 정보 삭제
    session.pop("auth_code", None)
    session.pop("auth_email", None)
    session.pop("auth_email_verified", None)

    return jsonify({"message": "비밀번호가 성공적으로 변경되었습니다."})

# --------------------- 사용자 목록 ---------------------

@app.route("/users")
def list_users():
    return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True)
