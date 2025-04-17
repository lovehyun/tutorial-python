import os
import re
import requests
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

# 기본 URL
BASE_URL = "https://www.moviechart.co.kr"
TARGET_URL = BASE_URL + "/rank/realtime/index/image"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 썸네일 저장 디렉토리
os.makedirs("thumbnails", exist_ok=True)

# 파일명 정리 함수 (금지 문자 제거)
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

# DB 연결
conn = sqlite3.connect("moviechart.db")
cur = conn.cursor()

# 테이블 생성
cur.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER,
    title TEXT UNIQUE,
    detail_link TEXT,
    thumbnail_path TEXT,
    original_url TEXT,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# HTML 요청 및 파싱
response = requests.get(TARGET_URL, headers=HEADERS)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 영화 카드 선택자
movie_cards = soup.select('div.movieBox li.movieBox-item')
print('무비카드 개수: ', len(movie_cards))

for idx, card in enumerate(movie_cards, start=1):
    title_tag = card.select_one('div.movie-title h3')
    img_tag = card.select_one('img')
    link_tag = card.select_one('a')

    title = title_tag.text.strip() if title_tag else "제목없음"
    detail_link = urljoin(BASE_URL, link_tag['href']) if link_tag and link_tag.has_attr('href') else ""
    thumb_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ""

    # 원본 이미지 URL 추출
    parsed = urlparse(thumb_url)
    query = parse_qs(parsed.query)
    original_url = query.get('source', [''])[0]  # 없는 경우는 빈 문자열

    # 썸네일 저장
    thumbnail_path = ''
    try:
        # 상대 경로라면 절대 경로로 변환
        if thumb_url.startswith('/'):
            thumb_url = urljoin(BASE_URL, thumb_url)
        image_data = requests.get(thumb_url, headers=HEADERS).content
        if len(image_data) > 0:
            safe_title = sanitize_filename(title)
            filename = f"thumbnails/{idx}_{safe_title}.jpg"
            with open(filename, 'wb') as f:
                f.write(image_data)
            thumbnail_path = filename
        else:
            print(f"[!] 썸네일이 비어 있음 (0바이트): {title}")
    except Exception as e:
        print(f"[!] 썸네일 다운로드 실패: {title} - {e}")
        thumbnail_path = ''

    print(f"{idx:2}. {title}")
    print(f"    썸네일 저장: {thumbnail_path}")
    print(f"    원본 URL: {original_url}")
    print(f"    상세 페이지: {detail_link}")

    # DB 저장 (중복 방지)
    try:
        cur.execute('''
        INSERT OR IGNORE INTO movies (rank, title, detail_link, thumbnail_path, original_url)
        VALUES (?, ?, ?, ?, ?)
        ''', (idx, title, detail_link, thumbnail_path, original_url))
    except Exception as e:
        print(f"[DB 오류] {title}: {e}")

conn.commit()
conn.close()
