import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# .env에서 값 가져오기
NAVER_EMAIL = os.getenv('NAVER_EMAIL')  # 네이버 이메일
NAVER_PASSWORD = os.getenv('NAVER_PASSWORD')  # 네이버 비밀번호 또는 앱 비밀번호

# SMTP 설정
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587

# 수신자 정보
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# 메일 내용
subject = '네이버 SMTP 메일 테스트'
body = '이 메일은 Python을 통해 네이버 SMTP 서버를 사용해 전송되었습니다.'

# MIMEText 객체 생성
message = MIMEText(body, _charset='utf-8')
message['Subject'] = subject
message['From'] = NAVER_EMAIL
message['To'] = RECIPIENT_EMAIL

try:
    # SMTP 서버 연결
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()  # TLS 보안 연결 시작
    smtp.login(NAVER_EMAIL, NAVER_PASSWORD)  # 로그인

    # 메일 전송
    smtp.sendmail(NAVER_EMAIL, RECIPIENT_EMAIL, message.as_string())
    print("메일이 성공적으로 전송되었습니다!")

except Exception as e:
    print(f"메일 전송 중 오류 발생: {e}")

finally:
    smtp.quit()  # 연결 종료
