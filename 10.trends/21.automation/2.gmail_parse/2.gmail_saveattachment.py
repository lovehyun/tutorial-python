# -*- coding: utf-8 -*-
"""
- .env에서 접두사/과제 키워드/저장폴더를 읽음
- 제목이 "[접두사] 과제명, OOO" 형태인 메일 검색
- OOO/보낸이/보낸시간 수집 + 엑셀 저장
- 각 메일의 첨부파일을 ATTACH_DIR/OOO_파일명 으로 저장
"""

import os
import re
import sys
import base64
import unicodedata
import pandas as pd
from pathlib import Path
from typing import List
from dateutil import tz
from email.utils import parseaddr, parsedate_to_datetime

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# ---------- 환경변수 ----------
load_dotenv()

CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")
TOKEN_PATH       = os.getenv("GOOGLE_TOKEN", "token.json")
OUTPUT_XLSX      = os.getenv("OUTPUT_XLSX", "bob14_mail_list.xlsx")

SUBJECT_PREFIX   = os.getenv("GMAIL_SUBJECT_PREFIX", "[BOB14]").strip()
ASSIGNMENTS_RAW  = os.getenv("GMAIL_ASSIGNMENTS", "도커과제,생성형AI과제")
QUERY_EXTRA      = os.getenv("GMAIL_QUERY_EXTRA", "").strip()

ATTACH_DIR       = os.getenv("ATTACH_DIR", "DATA").strip()
ATTACH_OVERWRITE = os.getenv("ATTACH_OVERWRITE", "0").strip() == "1"

ASSIGNMENTS: List[str] = [a.strip() for a in ASSIGNMENTS_RAW.split(",") if a.strip()]

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']  # 읽기 전용

# ---------- 유틸 ----------
def build_search_query(prefix: str, assignments: List[str], extra: str = "") -> str:
    terms = [f'(subject:"{prefix} {a}")' for a in assignments]
    base = " OR ".join(terms) if terms else f'subject:"{prefix}"'
    return f"{base} {extra}" if extra else base

def build_subject_patterns(prefix: str, assignments: List[str]) -> List[re.Pattern]:
    pfx = re.escape(prefix)
    patterns = [
        re.compile(rf'^\s*{pfx}\s*{re.escape(a)}\s*,\s*(.+)\s*$', re.IGNORECASE)
        for a in assignments
    ]
    # 범용 백업 패턴: [접두사] (쉼표 전까지 아무 과제명), OOO
    patterns.append(re.compile(rf'^\s*{pfx}\s*[^,]+,\s*(.+)\s*$', re.IGNORECASE))
    return patterns

def sanitize_filename(name: str) -> str:
    """파일명에 부적합 문자를 안전하게 치환"""
    name = unicodedata.normalize("NFKC", name)
    bad = r'\/:*?"<>|'
    for ch in bad:
        name = name.replace(ch, "_")
    # 일부 파일시스템 예약 이름 방지 (Windows)
    reserved = {"CON","PRN","AUX","NUL","COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9",
                "LPT1","LPT2","LPT3","LPT4","LPT5","LPT6","LPT7","LPT8","LPT9"}
    stem, ext = os.path.splitext(name)
    if stem.upper() in reserved:
        stem = f"_{stem}"
    return (stem + ext).strip().strip(".")

def ensure_unique_path(path: Path) -> Path:
    """덮어쓰기 옵션이 꺼져있을 때, 파일명이 중복이면 (1),(2)... 붙여서 회피"""
    if ATTACH_OVERWRITE or not path.exists():
        return path
    stem, ext = path.stem, path.suffix
    i = 1
    while True:
        cand = path.with_name(f"{stem} ({i}){ext}")
        if not cand.exists():
            return cand
        i += 1

# ---------- Gmail ----------
def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print(f"[오류] {CREDENTIALS_PATH} 이 없습니다. .env의 GOOGLE_CREDENTIALS 확인.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def list_all_messages(service, query, max_per_page=500):
    user_id = 'me'
    messages = []
    request = service.users().messages().list(userId=user_id, q=query, maxResults=max_per_page)
    while request is not None:
        resp = request.execute()
        messages.extend(resp.get('messages', []))
        request = service.users().messages().list_next(previous_request=request, previous_response=resp)
    # 중복 제거
    return list({m['id']: m for m in messages}.values())

def get_meta_headers(service, msg_id):
    user_id = 'me'
    resp = service.users().messages().get(
        userId=user_id,
        id=msg_id,
        format='metadata',
        metadataHeaders=['Subject', 'From', 'Date']
    ).execute()
    headers = {h['name']: h['value'] for h in resp.get('payload', {}).get('headers', [])}
    return headers.get('Subject', ''), headers.get('From', ''), headers.get('Date', '')

def get_full_message(service, msg_id):
    """첨부파일 파트 탐색을 위해 full 포맷으로 가져오기"""
    user_id = 'me'
    return service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()

def fetch_attachment_bytes(service, msg_id, attachment_id) -> bytes:
    user_id = 'me'
    att = service.users().messages().attachments().get(
        userId=user_id, messageId=msg_id, id=attachment_id
    ).execute()
    data = att.get('data', '')
    # base64url 디코드
    return base64.urlsafe_b64decode(data.encode('utf-8'))

def parse_from(from_raw: str):
    name, email = parseaddr(from_raw)
    return (name or "").strip(), (email or "").strip().lower()

def parse_date_to_seoul(date_raw: str) -> str:
    try:
        dt_utc = parsedate_to_datetime(date_raw)
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=tz.UTC)
        dt_seoul = dt_utc.astimezone(tz.gettz('Asia/Seoul'))
        return dt_seoul.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception:
        return ""

def extract_name_from_subject(subject: str, patterns: List[re.Pattern]) -> str:
    subj = subject or ""
    for p in patterns:
        m = p.match(subj)
        if m:
            return m.group(1).strip()
    return ""

def iter_attachments(payload) -> List[dict]:
    """payload 트리에서 첨부파일 파트만 추출: [{'filename','attachmentId','mimeType'}...]"""
    found = []

    def walk(part):
        if not part:
            return
        body = part.get('body', {})
        filename = (part.get('filename') or "").strip()
        mime = part.get('mimeType')
        # attachmentId가 있으면 첨부파일
        att_id = body.get('attachmentId')
        if filename and att_id:
            found.append({"filename": filename, "attachmentId": att_id, "mimeType": mime})
        # 하위 파트 재귀
        for child in part.get('parts', []) or []:
            walk(child)

    walk(payload)
    return found

# ---------- 메인 ----------
def main():
    # 준비
    gmail_query = build_search_query(SUBJECT_PREFIX, ASSIGNMENTS, QUERY_EXTRA)
    subject_patterns = build_subject_patterns(SUBJECT_PREFIX, ASSIGNMENTS)

    # 폴더 생성
    attach_root = Path(ATTACH_DIR)
    attach_root.mkdir(parents=True, exist_ok=True)

    service = get_gmail_service()
    print("▶ Gmail 검색 쿼리:", gmail_query)

    msgs = list_all_messages(service, gmail_query)
    print(f"▶ 검색된 메일 수: {len(msgs)}")

    rows = []
    total_saved = 0

    for m in msgs:
        msg_id = m['id']
        subject, from_raw, date_raw = get_meta_headers(service, msg_id)
        ooo = extract_name_from_subject(subject, subject_patterns) or "UNKNOWN"
        sender_name, sender_email = parse_from(from_raw)
        sent_at_seoul = parse_date_to_seoul(date_raw)

        # 첨부파일 처리
        full = get_full_message(service, msg_id)
        payload = full.get('payload', {})
        atts = iter_attachments(payload)

        saved_files = []
        for att in atts:
            raw_filename = att["filename"]
            safe_filename = sanitize_filename(raw_filename)
            prefixed = f"{ooo}_{safe_filename}"
            outpath = ensure_unique_path(attach_root / prefixed)

            try:
                data = fetch_attachment_bytes(service, msg_id, att["attachmentId"])
                outpath.write_bytes(data)
                saved_files.append(outpath.name)
                total_saved += 1
            except Exception as e:
                print(f"[경고] 첨부 저장 실패: msg={msg_id}, file={prefixed}, err={e}")

        rows.append({
            "Subject": subject,
            "OOO(제목에서 추출)": ooo,
            "FromName": sender_name,
            "FromEmail": sender_email,
            "Sent(Asia/Seoul)": sent_at_seoul,
            "MessageId": msg_id,
            "SavedAttachments": ", ".join(saved_files) if saved_files else ""
        })

    # 표/엑셀
    df = pd.DataFrame(rows, columns=[
        "Subject", "OOO(제목에서 추출)", "FromName", "FromEmail",
        "Sent(Asia/Seoul)", "MessageId", "SavedAttachments"
    ])

    if not df.empty:
        with pd.option_context('display.max_colwidth', 100):
            print("\n=== 결과 미리보기(상위 50건) ===")
            print(df.head(50).to_string(index=False))
    else:
        print("\n검색 결과가 없습니다.")

    df.to_excel(OUTPUT_XLSX, index=False, sheet_name="BOB14_Mails")
    print(f"\n▶ 엑셀 저장 완료: {OUTPUT_XLSX}")
    print(f"▶ 첨부파일 저장 폴더: {attach_root.resolve()}")
    print(f"▶ 저장된 첨부파일 수: {total_saved}")

if __name__ == "__main__":
    main()
