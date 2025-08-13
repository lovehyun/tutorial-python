import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

# 테스트 사용자 삽입 (비밀번호 해시 적용)
hashed_pw1 = hash_password('password1')
hashed_pw2 = hash_password('password2')

cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", 
            ('user1', hashed_pw1, 'UserName1'))
cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", 
            ('user2', hashed_pw2, 'UserName2'))

conn.commit()
conn.close()
