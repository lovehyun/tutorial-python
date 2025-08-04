# pip install flask flask-mail
# curl -X POST http://localhost:5000/send-code -H "Content-Type: application/json" -d '{"email": "test@example.com"}'
# curl -X POST http://localhost:5000/verify-code -H "Content-Type: application/json" -d '{"code": "123456"}'

from flask import Flask, request, session, jsonify, send_from_directory
from flask_mail import Mail, Message
import random
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 메일 설정
app.config['MAIL_SERVER'] = os.getenv("NAVER_MAILSERVER")
app.config['MAIL_PORT'] = os.getenv("NAVER_MAILSERVER_PORT")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("NAVER_EMAIL")  # Naver/Gmail 주소
app.config['MAIL_PASSWORD'] = os.getenv("NAVER_PASSWORD")  # 앱 비밀번호
mail = Mail(app)

@app.route("/")
def signup_page():
    return send_from_directory("static", "index.html")

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

    return jsonify({"message": "인증 코드가 전송되었습니다"})

# 인증 코드 검증
@app.route("/verify-code", methods=["POST"])
def verify_code():
    input_code = request.json.get("code")
    stored_code = session.get("auth_code")
    
    if stored_code == input_code:
        return jsonify({"message": "인증 성공"})
    return jsonify({"error": "인증 실패"}), 400

if __name__ == "__main__":
    app.run(debug=True)
