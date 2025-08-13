import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'users.db'

def create_user(username, password, name):
    hashed_pw = generate_password_hash(password)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                (username, hashed_pw, name))
    conn.commit()
    conn.close()

def init_database():
    # DB 및 테이블 생성
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    # 테스트 계정 생성
    create_user('user1', 'password1', 'UserName1')
    create_user('user2', 'password2', 'UserName2')

if __name__ == '__main__':
    init_database()
    print("users.db 초기화 완료: user1, user2 계정 생성됨 (werkzeug 기반 해시 사용)")
