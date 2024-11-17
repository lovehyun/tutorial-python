import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Gmail 계정 정보
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

def send_email(to_email, subject, body):
    try:
        # SMTP 서버 설정
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # 이메일 메시지 생성
        msg = MIMEText(body, _charset="utf-8")
        msg["Subject"] = subject
        msg["From"] = GMAIL_EMAIL
        msg["To"] = to_email

        # SMTP 서버 연결 및 로그인
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS 보안 연결
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)  # 로그인
            server.sendmail(GMAIL_EMAIL, to_email, msg.as_string())  # 메일 전송

        print(f"메일이 {to_email}로 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"메일 전송 실패: {e}")

# 예제 실행
if __name__ == "__main__":
    send_email(RECIPIENT_EMAIL, "테스트 메일", "이 메일은 테스트 목적으로 전송되었습니다.")
