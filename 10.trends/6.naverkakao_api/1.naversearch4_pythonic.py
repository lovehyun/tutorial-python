import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from tabulate import tabulate
import html
import re

# 환경변수 로드
load_dotenv()
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

def clean_html(raw_html):
    """HTML 태그 제거 및 이스케이프 해제"""
    text = re.sub("<.*?>", "", raw_html)  # <b>태그 제거
    return html.unescape(text)  # &quot; 같은 HTML 이스케이프 문자 해제

def search_naver_blog(query):
    """네이버 블로그 검색 API 호출 및 결과 반환"""
    encoded = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog?query={encoded}"

    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        with urllib.request.urlopen(req) as res:
            if res.status != 200:
                print("API 호출 실패:", res.status)
                return []
            data = json.loads(res.read())
            return data["items"]
    except Exception as e:
        print("요청 중 오류 발생:", e)
        return []

def print_results(items):
    """검색 결과를 표 형태로 출력"""
    rows = [["title", "link", "description"]]
    for item in items:
        title = clean_html(item["title"])
        desc = clean_html(item["description"])
        rows.append([title, item["link"], desc])
    print(tabulate(rows, headers="firstrow", tablefmt="grid"))

if __name__ == "__main__":
    query = "Python 개발"
    items = search_naver_blog(query)
    if items:
        print_results(items)
    else:
        print("검색 결과가 없습니다.")
