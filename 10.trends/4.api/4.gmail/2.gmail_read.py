import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Gmail 계정 정보
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def decode_mime_words(s):
    """MIME encoded words를 디코딩합니다."""
    decoded_string = ""
    for word, charset in decode_header(s):
        if isinstance(word, bytes):
            decoded_string += word.decode(charset or "utf-8", errors="replace")
        else:
            decoded_string += word
    return decoded_string

def read_emails(count=5):
    try:
        # Gmail IMAP 서버 연결
        imap_server = "imap.gmail.com"
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(GMAIL_EMAIL, GMAIL_PASSWORD)

        # 메일함 선택
        imap.select("inbox")

        # 메일 검색 (최신 5개)
        status, messages = imap.search(None, "ALL")
        # status, messages = imap.search(None, "UNSEEN") # 읽지 않은 메일

        if status != "OK":
            print("메일 검색 실패")
            return

        # 메일 ID 가져오기
        mail_ids = messages[0].split()
        latest_mail_ids = mail_ids[-count:]  # 입력된 개수만큼 최신 메일 가져오기

        for index, mail_id in enumerate(reversed(latest_mail_ids), start=1):
            status, msg_data = imap.fetch(mail_id, "(RFC822)")
            if status != "OK":
                print(f"메일 {mail_id.decode()} 가져오기 실패")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 메일 제목 디코딩
                    subject = decode_mime_words(msg["Subject"] or "제목 없음")

                    # 발신자 디코딩
                    from_ = decode_mime_words(msg.get("From") or "발신자 없음")

                    # 본문 추출
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="replace")

                    # 메일 구분자 출력
                    print(f">>>>>>>>>> 메일번호 {index} <<<<<<<<<<")
                    # 메일 정보 출력
                    print(f"제목: {subject}")
                    print(f"발신자: {from_}")
                    print(f"본문: {body}")
                    print("=" * 50)

        # IMAP 연결 종료
        imap.logout()

    except Exception as e:
        print(f"메일 읽기 실패: {e}")

# 예제 실행
if __name__ == "__main__":
    # 최신 3개의 메일 읽기
    read_emails(count=3)
