import smtplib
from email.mime.text import MIMEText

# 네이버 SMTP 설정
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587

# 네이버 계정 정보
NAVER_ID = 'your_naver_id'  # 네이버 아이디 (이메일 주소의 @naver.com 제외)
NAVER_EMAIL = f'{NAVER_ID}@naver.com'  # 전체 이메일 주소
NAVER_PASSWORD = 'your_password'  # 네이버 로그인 비밀번호 또는 앱 비밀번호

# 수신자 정보
recipient_email = 'recipient@example.com'

# 메일 내용
subject = '네이버 SMTP 메일 테스트'
body = '이 메일은 Python을 통해 네이버 SMTP 서버를 사용해 전송되었습니다.'

# MIMEText 객체 생성
message = MIMEText(body, _charset='utf-8')
message['Subject'] = subject
message['From'] = NAVER_EMAIL
message['To'] = recipient_email

try:
    # SMTP 서버에 연결
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()  # TLS 보안 연결 시작
    smtp.login(NAVER_EMAIL, NAVER_PASSWORD)  # 로그인

    # 메일 전송
    smtp.sendmail(NAVER_EMAIL, recipient_email, message.as_string())
    print("메일이 성공적으로 전송되었습니다!")

except Exception as e:
    print(f"메일 전송 중 오류 발생: {e}")

finally:
    smtp.quit()  # 연결 종료
