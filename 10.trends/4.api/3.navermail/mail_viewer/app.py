from flask import Flask, render_template, jsonify
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

# Flask 앱 생성
app = Flask(__name__)

# 환경 변수 로드
load_dotenv()

# 네이버 계정 정보
NAVER_EMAIL = os.getenv("NAVER_EMAIL")
NAVER_PASSWORD = os.getenv("NAVER_PASSWORD")

# IMAP 서버 정보
IMAP_SERVER = 'imap.naver.com'
IMAP_PORT = 993

# MIME 디코딩 헬퍼 함수
def decode_mime_words(s):
    decoded_string = ""
    for word, charset in decode_header(s):
        if isinstance(word, bytes):
            decoded_string += word.decode(charset or "utf-8", errors="replace")
        else:
            decoded_string += word
    return decoded_string

# IMAP 서버 연결 및 로그인 함수
def connect_to_mailbox():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(NAVER_EMAIL, NAVER_PASSWORD)
        return mail
    except Exception as e:
        print(f"메일 서버 연결 실패: {e}")
        return None

# 메일 목록 가져오기
def fetch_mail_list():
    try:
        mail = connect_to_mailbox()
        if not mail:
            return []

        mail.select("INBOX")
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return []

        mail_ids = messages[0].split()
        mail_list = []

        # 최신 10개 메일 가져오기
        for mail_id in reversed(mail_ids[-10:]):
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            if status != "OK":
                continue
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_mime_words(msg["Subject"] or "제목 없음")
                    from_ = decode_mime_words(msg.get("From") or "발신자 없음")
                    mail_list.append({
                        "id": mail_id.decode("utf-8"),
                        "subject": subject,
                        "from": from_
                    })
        mail.logout()
        return mail_list
    except Exception as e:
        print(f"메일 목록 가져오기 실패: {e}")
        return []

# 특정 메일 가져오기
def fetch_mail(mail_id):
    try:
        mail = connect_to_mailbox()
        if not mail:
            return None

        mail.select("INBOX")
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        if status != "OK":
            return None

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_mime_words(msg["Subject"] or "제목 없음")
                from_ = decode_mime_words(msg.get("From") or "발신자 없음")
                body = "[내용 없음]"  # 기본값 설정
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                            break
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                mail.logout()
                return {"subject": subject, "from": from_, "body": body}
    except Exception as e:
        print(f"메일 가져오기 실패: {e}")
        return None

# 메일 목록 페이지
@app.route("/")
def index():
    mail_list = fetch_mail_list()
    return render_template("index.html", mail_list=mail_list)

# 특정 메일 상세 데이터 API
@app.route("/mail/<mail_id>")
def mail_detail(mail_id):
    mail = fetch_mail(mail_id)
    if not mail:
        return jsonify({"error": "메일을 불러올 수 없습니다."}), 404
    return jsonify(mail)

if __name__ == "__main__":
    app.run(debug=True)
