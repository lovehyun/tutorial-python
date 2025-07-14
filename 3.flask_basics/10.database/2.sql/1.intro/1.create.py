import sqlite3

# 데이터베이스 연결 (파일 기반)
conn = sqlite3.connect('example.db')

# 커서 객체 생성
cur = conn.cursor()

# 테이블 생성
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')

# 커밋하여 변경사항 저장
conn.commit()

# 데이터베이스 연결 닫기
conn.close()
