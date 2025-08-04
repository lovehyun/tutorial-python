# pip install flask flask-mail python-dotenv
# curl -X POST http://127.0.0.1:5000/send-code -H "Content-Type: application/json" -d '{"email": "you@example.com"}' -c cookies.txt
# curl -X POST http://127.0.0.1:5000/verify-code -H "Content-Type: application/json" -d '{"code": "384920"}' -b cookies.txt

from flask import Flask, request, session, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import random
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 메일 설정
app.config['MAIL_SERVER'] = os.getenv("NAVER_MAILSERVER")
app.config['MAIL_PORT'] = os.getenv("NAVER_MAILSERVER_PORT")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("NAVER_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("NAVER_PASSWORD")

mail = Mail(app)

# 간단한 메일 전송 테스트
@app.route("/send")
def send_mail():
    msg = Message(
        "제목입니다",
        sender=app.config['MAIL_USERNAME'],
        recipients=["you@example.com"],  # 테스트 받을 이메일 주소
        body="이메일 본문 내용입니다."
    )
    mail.send(msg)
    return "메일 전송 완료!"

# 인증 코드 발송
@app.route("/send-code", methods=["POST"])
def send_code():
    email = request.json.get("email")
    if not email:
        return jsonify({"error": "이메일을 입력해주세요"}), 400

    code = str(random.randint(100000, 999999))
    session["auth_code"] = code
    session["auth_email"] = email
    session["auth_email_verified"] = False

    # 메일 전송
    msg = Message("회원가입 인증 코드", sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"인증 코드: {code}"
    mail.send(msg)

    print(f"[DEBUG] 인증코드 발송 대상 이메일: {email}, 코드: {code}")

    return jsonify({"message": "인증 코드가 전송되었습니다"})

# 인증 코드 검증
@app.route("/verify-code", methods=["POST"])
def verify_code():
    input_code = request.json.get("code")
    stored_code = session.get("auth_code")
    email = session.get("auth_email")

    print(f"[DEBUG] 세션에 저장된 인증코드: {stored_code}, 사용자 입력: {input_code}")

    if stored_code == input_code:
        session["auth_email_verified"] = True
        session["verified_email"] = email
        return jsonify({"message": "인증 성공"})

    return jsonify({"error": "인증 실패"}), 400

# 세션 확인 (디버그용)
@app.route("/session")
def session_info():
    return jsonify(dict(session))

if __name__ == "__main__":
    app.run(debug=True)
