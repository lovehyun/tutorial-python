import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()

# users 테이블 생성
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL
)
''')

# 테스트 사용자 삽입
cur.execute("INSERT OR IGNORE INTO users (username, password, name) VALUES (?, ?, ?)",
            ('user', 'password', 'MyName'))

conn.commit()
conn.close()
