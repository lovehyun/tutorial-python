import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('movie_data.db')
cur = conn.cursor()

# 테이블 생성
cur.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    rating TEXT,
    reservation_rate TEXT,
    poster_link_url TEXT,
    short_description TEXT
)
''')

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
data = requests.get('https://movie.daum.net/ranking/reservation', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# 영화 목록 가져오기
movies = soup.select('#mainContent > div > div.box_ranking > ol > li')

# 각 영화의 정보를 DB에 저장하기
for movie in movies:
    title_tag = movie.select_one('div > div.thumb_cont > strong')
    rating_tag = movie.select_one('div > div.thumb_cont > span.txt_append > span:nth-child(1)')
    reservation_rate_tag = movie.select_one('div > div.thumb_cont > span.txt_append > span:nth-child(2)')
    movie_selected = movie.select_one('div > div.thumb_item > div.poster_info > a')

    if title_tag and rating_tag and reservation_rate_tag and movie_selected:
        movie_title = title_tag.text.strip()
        # movie_rating = rating_tag.text.strip()
        movie_rating = float(rating_tag.text.strip().replace("평점", ""))
        # reservation_rate = reservation_rate_tag.text.strip()
        reservation_rate = float(reservation_rate_tag.text.strip().replace("예매율", "").replace("%", ""))

        relative_url = movie_selected['href']
        poster_link_url = urljoin('https://movie.daum.net', relative_url)
        short_description = movie_selected.text.strip()

        # 데이터 삽입
        cur.execute('INSERT INTO movies (title, rating, reservation_rate, poster_link_url, short_description) VALUES (?, ?, ?, ?, ?)',
                    (movie_title, movie_rating, reservation_rate, poster_link_url, short_description))

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()
