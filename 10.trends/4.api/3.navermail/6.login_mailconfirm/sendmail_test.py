# pip install flask flask-mail

from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# 메일 설정 (네이버 SMTP)
app.config['MAIL_SERVER'] = os.getenv("NAVER_MAILSERVER")
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("NAVER_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("NAVER_PASSWORD")

mail = Mail(app)

@app.route("/send")
def send_mail():
    msg = Message("제목입니다", sender=app.config['MAIL_USERNAME'],
                  recipients=["you@example.com"], body="이메일 본문 내용입니다.")
    mail.send(msg)
    return "메일 전송 완료!"

if __name__ == "__main__":
    app.run(debug=True)
