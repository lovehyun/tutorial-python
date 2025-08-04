from flask import Flask, jsonify, render_template
from imapclient import IMAPClient
from email import message_from_bytes
from email.header import decode_header
from dotenv import load_dotenv
import os

load_dotenv()

IMAP_HOST = os.getenv("NAVER_IMAP_SERVER")
IMAP_PORT = int(os.getenv("NAVER_IMAP_PORT"))
EMAIL_ID = os.getenv("NAVER_EMAIL")
EMAIL_PASSWORD = os.getenv("NAVER_PASSWORD")

app = Flask(__name__)

def decode_mime(s):
    if not s:
        return ""
    parts = decode_header(s)
    decoded = ''
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded += part.decode(charset or 'utf-8', errors='replace')
        else:
            decoded += part
    return decoded

def fetch_emails():
    try:
        with IMAPClient(IMAP_HOST, ssl=True, port=IMAP_PORT) as server:
            server.login(EMAIL_ID, EMAIL_PASSWORD)
            server.select_folder("INBOX", readonly=True)
            messages = server.search(['ALL'])

            results = []
            for uid in reversed(messages[-10:]):
                raw_msg = server.fetch([uid], ['RFC822'])[uid][b'RFC822']
                msg = message_from_bytes(raw_msg)

                subject = decode_mime(msg.get("Subject", "제목 없음"))
                from_ = decode_mime(msg.get("From", "발신자 없음"))

                body = "[내용 없음]"
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                                break
                            except Exception:
                                continue
                else:
                    body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace')

                results.append({
                    "uid": uid,
                    "from": from_,
                    "subject": subject,
                    "body_preview": body[:200].replace("\n", " ")
                })
            return results
    except Exception as e:
        print("메일 수신 오류:", e)
        return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/emails")
def api_emails():
    return jsonify(fetch_emails())

if __name__ == "__main__":
    app.run(debug=True)
