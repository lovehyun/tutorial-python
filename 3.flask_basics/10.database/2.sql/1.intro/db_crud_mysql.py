# pip install mysql-connector-python

#  '?' → %s 로 변경해야 함
# (sqlite3는 ?, mysql.connector는 %s를 플레이스홀더로 사용)
# 
# 연결 정보는 .env에 넣는 게 좋습니다:
#
# import os
# from dotenv import load_dotenv
# load_dotenv()
#
# DB_CONFIG = {
#     "host": "localhost",
#     "user": "root",
#     "password": "your_password",
#     "database": "example_db",
#     "charset": "utf8mb4"
# }
#
# DB_CONFIG = {
#     "host": os.getenv("MYSQL_HOST", "localhost"),
#     "user": os.getenv("MYSQL_USER", "root"),
#     "password": os.getenv("MYSQL_PASSWORD", "secret"),
#     "database": os.getenv("MYSQL_DATABASE", "example_db"),
#     "charset": "utf8mb4"
# }
#
# def connect_db():
#     """DB_CONFIG를 이용한 MySQL 연결"""
#     return mysql.connector.connect(**DB_CONFIG)


import mysql.connector

# ─────────────────────────────────────────────
# 1. 데이터베이스 연결 함수
# ─────────────────────────────────────────────
# def connect_db():
#     """MySQL 연결 반환"""
#     return mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST", "localhost"),
#         user=os.getenv("MYSQL_USER", "root"),
#         password=os.getenv("MYSQL_PASSWORD", "secret"),
#         database=os.getenv("MYSQL_DATABASE", "example_db"),
#         charset="utf8mb4",
#     )

def connect_db():
    """MySQL 직접 설정 연결 반환 (.env 없이)"""
    return mysql.connector.connect(
        host="localhost",            # 실제 호스트 주소
        user="root",                 # MySQL 사용자 이름
        password="your_password",    # 실제 비밀번호
        database="example_db",       # 사용할 데이터베이스 이름
        charset="utf8mb4"            # 한글 포함 문자열 대응
    )
# ─────────────────────────────────────────────
# 2. 테이블 생성
# ─────────────────────────────────────────────
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id   INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age  INT          NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# ─────────────────────────────────────────────
# 3. CREATE (삽입)
# ─────────────────────────────────────────────
def insert_user(name: str, age: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cur.close()
    conn.close()

# ─────────────────────────────────────────────
# 4. READ (조회)
# ─────────────────────────────────────────────
def get_users():
    conn = connect_db()
    cur = conn.cursor()                     # Tuple 이 기본값
    # cur = conn.cursor(dictionary=True)    # dict 형태 반환
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_user_by_name(name: str):
    conn = connect_db()
    cur = conn.cursor()
    # cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE name = %s", (name,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

# ─────────────────────────────────────────────
# 5. UPDATE (수정)
# ─────────────────────────────────────────────
def update_user(name: str, new_age: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET age = %s WHERE name = %s", (new_age, name))
    conn.commit()
    cur.close()
    conn.close()

# ─────────────────────────────────────────────
# 6. DELETE (삭제)
# ─────────────────────────────────────────────
def delete_user_by_name(name: str):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE name = %s", (name,))
    conn.commit()
    cur.close()
    conn.close()

def delete_user_by_id(user_id: int):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
