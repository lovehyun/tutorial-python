import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# IMAP 서버 정보
IMAP_SERVER = 'imap.naver.com'
IMAP_PORT = 993

# 사용자 정보
# .env에서 값 가져오기
NAVER_EMAIL = os.getenv('NAVER_EMAIL')  # 네이버 이메일
NAVER_PASSWORD = os.getenv('NAVER_PASSWORD')  # 네이버 비밀번호 또는 앱 비밀번호

# 디코딩 헬퍼 함수
def decode_mime_words(s):
    """
    MIME encoded words를 디코딩합니다.
    """
    decoded_string = ""
    for word, charset in decode_header(s):
        if isinstance(word, bytes):
            try:
                decoded_string += word.decode(charset or "utf-8", errors="replace")
            except Exception:
                decoded_string += word.decode("euc-kr", errors="replace")
        else:
            decoded_string += word
    return decoded_string

# 최근 5개의 메일 읽기
def read_latest_emails(count=5):
    try:
        # IMAP 서버 연결
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(NAVER_EMAIL, NAVER_PASSWORD)
        
        # 메일함 선택 (기본 메일함: INBOX)
        mail.select("INBOX")

        # 메일 검색 (모든 메일 가져오기)
        status, messages = mail.search(None, "ALL")

        # 검색 결과가 비어있지 않은지 확인
        if status != "OK" or not messages[0]:
            print("메일이 없습니다.")
            return

        # 메일 ID 목록 가져오기 (최신 메일 ID)
        mail_ids = messages[0].split()
        latest_mail_ids = mail_ids[-count:]  # 최신 메일 N개 가져오기

        for idx, mail_id in enumerate(reversed(latest_mail_ids), start=1):  # 최신 메일부터 처리
            # 최신 메일 가져오기
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            if status != "OK":
                print(f"{idx}번째 메일 가져오기 실패.")
                continue

            print(f"{'>' * 20} {idx}번째 메일 시작 {'<' * 20}")

            # 메일 데이터 파싱
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # 메일 데이터 디코딩
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 제목 디코딩
                    raw_subject = msg["Subject"]
                    subject = decode_mime_words(raw_subject) if raw_subject else "제목 없음"

                    print(f"제목: {subject}")
                    
                    # 발신자 정보
                    from_ = msg.get("From")
                    print(f"발신자: {from_}")

                    # 메일 본문 추출
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                try:
                                    body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                                except Exception:
                                    body = "[본문 디코딩 실패]"
                                print(f"본문: {body}")
                                break
                    else:
                        # 단일 파트 메일
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                        except Exception:
                            body = "[본문 디코딩 실패]"
                        print(f"본문: {body}")
                
            # 메일 구분자 출력
            print(f"{'>' * 20} {idx}번째 메일  끝  {'<' * 20}")

        # 연결 종료
        mail.logout()

    except Exception as e:
        print(f"오류 발생: {e}")

# 최근 5개의 메일 읽기 실행
read_latest_emails(5)
