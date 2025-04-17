import sqlite3

# 데이터베이스 연결 및 테이블 생성 함수
def init_db():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank TEXT NOT NULL,
            title TEXT NOT NULL,
            audience TEXT NOT NULL,
            link TEXT
        )
    ''')
    conn.commit()
    return conn, cur

# 데이터베이스에 영화 데이터 저장 함수
def save_to_db(conn, cur, rank, title, audience, link=""):
    cur.execute('''
        INSERT INTO movies (rank, title, audience, link)
        VALUES (?, ?, ?, ?)
    ''', (rank, title, audience, link))
    conn.commit()

# 데이터베이스의 내용을 조회하여 화면에 출력하는 함수
def query_and_display_movies(cur):
    cur.execute('SELECT rank, title, audience FROM movies')
    rows = cur.fetchall()
    for row in rows:
        print(f"순위: {row[0]}, 영화 제목: {row[1]}, 관객 수: {row[2]}")

# 데이터베이스 연결 종료 함수
def close_db(conn):
    conn.close()
