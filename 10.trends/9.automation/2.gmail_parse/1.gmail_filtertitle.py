# -*- coding: utf-8 -*-
"""
[기능]
- .env에서 접두사/과제 키워드를 읽어, Gmail 제목이 "[접두사] 과제명, OOO" 형태인 메일 전체 검색
- 제목에서 OOO 추출, 보낸이 이름/이메일, 보낸 시간(Asia/Seoul) 추출
- 콘솔 표 출력 + 엑셀(xlsx) 저장

[필요 파일]
- credentials.json (OAuth 클라이언트 ID)  ※ 경로는 .env의 GOOGLE_CREDENTIALS로 지정

[설치]
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas openpyxl python-dateutil python-dotenv
"""

import os
import re
import sys
import pandas as pd
from dateutil import tz
from email.utils import parseaddr, parsedate_to_datetime

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# ---------- 환경변수 로드 ----------
load_dotenv()

CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")
TOKEN_PATH       = os.getenv("GOOGLE_TOKEN", "token.json")
OUTPUT_XLSX      = os.getenv("OUTPUT_XLSX", "bob14_mail_list.xlsx")

SUBJECT_PREFIX   = os.getenv("GMAIL_SUBJECT_PREFIX", "[BOB14]").strip()
ASSIGNMENTS_RAW  = os.getenv("GMAIL_ASSIGNMENTS", "도커과제,생성형AI과제")
QUERY_EXTRA      = os.getenv("GMAIL_QUERY_EXTRA", "").strip()

# 과제 키워드 목록 (공백/빈 항목 제거)
ASSIGNMENTS = [a.strip() for a in ASSIGNMENTS_RAW.split(",") if a.strip()]

# ---------- Gmail API 범위(읽기 전용) ----------
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def build_search_query(prefix: str, assignments: list[str], extra: str = "") -> str:
    """
    Gmail 검색 쿼리 생성.
    예) (subject:"[BOB14] 도커과제") OR (subject:"[BOB14] 생성형AI과제") newer_than:30d
    """
    terms = [f'(subject:"{prefix} {a}")' for a in assignments]
    base = " OR ".join(terms) if terms else f'subject:"{prefix}"'
    if extra:
        return f"{base} {extra}"
    return base


def build_subject_patterns(prefix: str, assignments: list[str]) -> list[re.Pattern]:
    """
    제목 정규식 패턴 목록 생성: r'^\s*\[BOB14\]\s*도커과제,\s*(.+)\s*$'
    과제별로 한 개씩, 매칭 실패 시를 대비한 범용 패턴 하나를 추가.
    """
    escaped_prefix = re.escape(prefix)
    patterns = [
        re.compile(rf'^\s*{escaped_prefix}\s*{re.escape(a)}\s*,\s*(.+)\s*$', re.IGNORECASE)
        for a in assignments
    ]
    # 범용: [접두사] (쉼표 전까지 어떤 과제명), OOO
    patterns.append(re.compile(rf'^\s*{escaped_prefix}\s*[^,]+,\s*(.+)\s*$', re.IGNORECASE))
    return patterns


def get_gmail_service():
    """OAuth 인증을 수행하고 Gmail API 서비스 객체를 반환합니다."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print(f"[오류] {CREDENTIALS_PATH} 파일이 없습니다. .env의 GOOGLE_CREDENTIALS를 확인하세요.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def list_all_messages(service, query, max_per_page=500):
    """쿼리에 맞는 모든 메시지 ID 수집(페이지네이션)."""
    user_id = 'me'
    messages = []
    request = service.users().messages().list(userId=user_id, q=query, maxResults=max_per_page)
    while request is not None:
        resp = request.execute()
        messages.extend(resp.get('messages', []))
        request = service.users().messages().list_next(previous_request=request, previous_response=resp)
    # 중복 제거(같은 메일이 여러 조건에 걸렸을 때 대비)
    uniq = {m['id']: m for m in messages}
    return list(uniq.values())


def get_meta_headers(service, msg_id):
    """필요 헤더만 가져오기."""
    user_id = 'me'
    resp = service.users().messages().get(
        userId=user_id,
        id=msg_id,
        format='metadata',
        metadataHeaders=['Subject', 'From', 'Date']
    ).execute()
    headers = {h['name']: h['value'] for h in resp.get('payload', {}).get('headers', [])}
    return headers.get('Subject', ''), headers.get('From', ''), headers.get('Date', '')


def parse_from(from_raw: str) -> tuple[str, str]:
    """From 헤더에서 보낸이 이름/이메일 분리."""
    name, email = parseaddr(from_raw)
    return (name or "").strip(), (email or "").strip().lower()


def parse_date_to_seoul(date_raw: str) -> str:
    """Date 헤더를 Asia/Seoul로 변환."""
    try:
        dt_utc = parsedate_to_datetime(date_raw)
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=tz.UTC)
        dt_seoul = dt_utc.astimezone(tz.gettz('Asia/Seoul'))
        return dt_seoul.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception:
        return ""


def extract_name_from_subject(subject: str, patterns: list[re.Pattern]) -> str:
    """여러 패턴을 순서대로 시도하여 OOO(이름) 추출."""
    subj = subject or ""
    for p in patterns:
        m = p.match(subj)
        if m:
            return m.group(1).strip()
    return ""


def main():
    # 검색 쿼리/정규식 준비
    gmail_query = build_search_query(SUBJECT_PREFIX, ASSIGNMENTS, QUERY_EXTRA)
    subject_patterns = build_subject_patterns(SUBJECT_PREFIX, ASSIGNMENTS)

    service = get_gmail_service()
    print("▶ Gmail 검색 쿼리:", gmail_query)

    msgs = list_all_messages(service, gmail_query)
    print(f"▶ 검색된 메일 수: {len(msgs)}")

    rows = []
    for m in msgs:
        subject, from_raw, date_raw = get_meta_headers(service, m['id'])
        ooo_name = extract_name_from_subject(subject, subject_patterns)
        sender_name, sender_email = parse_from(from_raw)
        sent_at_seoul = parse_date_to_seoul(date_raw)
        rows.append({
            "Subject": subject,
            "OOO(제목에서 추출)": ooo_name,
            "FromName": sender_name,
            "FromEmail": sender_email,
            "Sent(Asia/Seoul)": sent_at_seoul,
            "MessageId": m['id'],
        })

    df = pd.DataFrame(rows, columns=[
        "Subject", "OOO(제목에서 추출)", "FromName", "FromEmail", "Sent(Asia/Seoul)", "MessageId"
    ])

    if not df.empty:
        with pd.option_context('display.max_colwidth', 100):
            print("\n=== 결과 미리보기(상위 50건) ===")
            print(df.head(50).to_string(index=False))
    else:
        print("\n검색 결과가 없습니다.")

    df.to_excel(OUTPUT_XLSX, index=False, sheet_name="BOB14_Mails")
    print(f"\n▶ 엑셀 저장 완료: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
