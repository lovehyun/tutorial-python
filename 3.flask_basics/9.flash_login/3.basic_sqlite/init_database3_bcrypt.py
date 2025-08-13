import sqlite3
import bcrypt

DB_PATH = 'users.db'

# 사용자 생성 (bcrypt 해시 적용)
def create_user(username, password, name):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                (username, hashed_pw, name))
    conn.commit()
    conn.close()

# 데이터베이스 초기화 함수
def init_database():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # users 테이블 생성 (비밀번호는 BLOB 타입)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        name TEXT NOT NULL
    )
    ''')
    conn.commit()

    # 테스트 사용자 삽입
    create_user('user1', 'password1', 'UserName1')
    create_user('user2', 'password2', 'UserName2')

    conn.close()

# 스크립트 직접 실행 시
if __name__ == '__main__':
    init_database()
    print("users.db 초기화 완료: user1, user2 계정이 bcrypt 해시로 생성됨")
