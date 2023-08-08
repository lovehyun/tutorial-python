import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin
from datetime import date

# 데이터베이스 연결 및 테이블 생성
def create_table():
    conn = sqlite3.connect('movie_rankings.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        poster_img_url TEXT,
                        poster_link_url TEXT,
                        short_description TEXT
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS weekly_rankings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fetch_date DATE NOT NULL,
                        movie_id INTEGER NOT NULL,
                        ranking INTEGER,
                        rating REAL,
                        reservation_rate REAL,
                        FOREIGN KEY (movie_id) REFERENCES movies(id)
                      )''')

    conn.close()

# 영화 정보 가져오기
def get_movie_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.daum.net/ranking/reservation', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    movies = soup.select('#mainContent > div > div.box_ranking > ol > li')

    movie_data = []
    for movie in movies:
        title_tag = movie.select_one('div > div.thumb_cont > strong')
        if title_tag:
            movie_title = title_tag.text.strip()
            movie_selected = movie.select_one('div > div.thumb_item')
            if movie_selected:
                poster_img = movie_selected.select_one('div.poster_movie > img')
                poster_img_url = poster_img['src']
                poster_link = movie_selected.select_one('div.poster_info > a')
                relative_url = poster_link['href']
                poster_link_url = urljoin('https://movie.daum.net', relative_url)
                short_description = movie_selected.text.strip()

                movie_data.append({
                    'title': movie_title,
                    'poster_img_url': poster_img_url,
                    'poster_link_url': poster_link_url,
                    'short_description': short_description,
                    'soup': movie  # 추후 파싱을 위한 추가 데이터 임시 저장
                })

    return movie_data

# 영화 정보를 데이터베이스에 삽입
def insert_movie_data(movie_data):
    conn = sqlite3.connect('movie_rankings.db')
    cursor = conn.cursor()

    for movie in movie_data:
        cursor.execute('''INSERT INTO movies (title, poster_img_url, poster_link_url, short_description)
                          VALUES (?, ?, ?, ?)''', (movie['title'], movie['poster_img_url'], movie['poster_link_url'], movie['short_description']))
        conn.commit()

    conn.close()

# 주간 랭킹 데이터를 데이터베이스에 삽입
def insert_weekly_rankings(movie_data):
    conn = sqlite3.connect('movie_rankings.db')
    cursor = conn.cursor()

    fetch_date = date.today()

    for idx, movie in enumerate(movie_data, 1):
        cursor.execute('SELECT id FROM movies WHERE title=?', (movie['title'],))
        movie_id = cursor.fetchone()[0]

        rating_tag = movie['soup'].select_one('div > div.thumb_cont > span.txt_append > span:nth-child(1)')
        reservation_rate_tag = movie['soup'].select_one('div > div.thumb_cont > span.txt_append > span:nth-child(2)')

        movie_rating = float(rating_tag.text.strip().replace("평점", "")) if rating_tag else None
        reservation_rate = float(reservation_rate_tag.text.strip().replace("예매율", "").replace("%", "")) if reservation_rate_tag else None

        cursor.execute('''INSERT INTO weekly_rankings (fetch_date, movie_id, ranking, rating, reservation_rate)
                          VALUES (?, ?, ?, ?, ?)''', (fetch_date, movie_id, idx, movie_rating, reservation_rate))
        conn.commit()

    conn.close()

def main():
    create_table()
    movie_data = get_movie_data()
    # print(movie_data)
    insert_movie_data(movie_data)
    insert_weekly_rankings(movie_data)

if __name__ == '__main__':
    main()
