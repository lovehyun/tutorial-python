from dotenv import load_dotenv
from tabulate import tabulate
import os
import requests
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
    url = "https://openapi.naver.com/v1/search/blog"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {"query": query}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
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
