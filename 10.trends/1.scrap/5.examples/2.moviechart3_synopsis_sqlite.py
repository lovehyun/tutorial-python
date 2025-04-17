import os
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

# 설정
BASE_URL = "https://www.moviechart.co.kr"
TARGET_URL = BASE_URL + "/rank/realtime/index/image"
HEADERS = {"User-Agent": "Mozilla/5.0"}
DB_PATH = "moviechart.db"
THUMBNAIL_DIR = "thumbnails"

# 디렉토리 생성
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# 파일명 정리 함수
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

# 시놉시스 가져오기
def get_synopsis(detail_url):
    try:
        res = requests.get(detail_url, headers=HEADERS)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            box = soup.select_one("div.contentBox div.text")
            return box.text.strip() if box else ''
    except Exception as e:
        print(f"[!] 시놉시스 수집 실패: {detail_url} - {e}")
    return ''

# DB 설정 및 테이블 생성
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank INTEGER,
        title TEXT UNIQUE,
        detail_link TEXT,
        thumbnail_path TEXT,
        original_url TEXT,
        synopsis TEXT,
        scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    return conn, cur

# 영화 목록 스크래핑
def scrape_movies():
    response = requests.get(TARGET_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    movie_cards = soup.select('div.movieBox li.movieBox-item')
    print(f"🎞️ 무비카드 개수: {len(movie_cards)}")
    return movie_cards

# 영화 1개 저장
def process_movie(card, idx, cur):
    title_tag = card.select_one('div.movie-title h3')
    img_tag = card.select_one('img')
    link_tag = card.select_one('a')

    title = title_tag.text.strip() if title_tag else "제목없음"
    detail_link = urljoin(BASE_URL, link_tag['href']) if link_tag and link_tag.has_attr('href') else ""
    thumb_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ""

    # 원본 이미지 URL 추출
    parsed = urlparse(thumb_url)
    query = parse_qs(parsed.query)
    original_url = query.get('source', [''])[0]

    # 썸네일 저장
    thumbnail_path = ''
    try:
        if thumb_url.startswith('/'):
            thumb_url = urljoin(BASE_URL, thumb_url)
        image_data = requests.get(thumb_url, headers=HEADERS).content
        if len(image_data) > 0:
            filename = f"{THUMBNAIL_DIR}/{idx}_{sanitize_filename(title)}.jpg"
            with open(filename, 'wb') as f:
                f.write(image_data)
            thumbnail_path = filename
        else:
            print(f"[!] 썸네일 없음 (0바이트): {title}")
    except Exception as e:
        print(f"[!] 썸네일 저장 실패: {title} - {e}")

    # 시놉시스 가져오기
    synopsis = get_synopsis(detail_link)

    # 출력
    print(f"{idx:2}. {title}")
    print(f"    썸네일: {thumbnail_path}")
    print(f"    원본 이미지: {original_url}")
    print(f"    상세 링크: {detail_link}")
    print(f"    시놉시스: {synopsis[:100]}...") # 100글자만 출력

    # DB 삽입
    try:
        cur.execute('''
        INSERT OR IGNORE INTO movies (rank, title, detail_link, thumbnail_path, original_url, synopsis)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (idx, title, detail_link, thumbnail_path, original_url, synopsis))
    except Exception as e:
        print(f"[DB 오류] {title}: {e}")

# 메인 실행 함수
def main():
    conn, cur = setup_database()
    cards = scrape_movies()
    for idx, card in enumerate(cards, start=1):
        process_movie(card, idx, cur)
    conn.commit()
    conn.close()

# 실행
if __name__ == "__main__":
    main()
