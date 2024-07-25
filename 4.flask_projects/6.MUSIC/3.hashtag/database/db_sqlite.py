import sqlite3
import os

# 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'music.db')

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.row_factory = sqlite3.Row
    return conn

# SQL 파일 실행 함수
def execute_sql_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        
# SQLite3 데이터베이스 초기화
def init_db():
    sql_file_path = os.path.join(BASE_DIR, 'init_sqlite3.sql')
    execute_sql_file(sql_file_path)

def query_db(query, args=(), one=False):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        r = cursor.fetchall()
        conn.commit()
        return (r[0] if r else None) if one else r

def execute_db(query, args=()):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

def get_notification_count(user_id):
    result = query_db('SELECT COUNT(*) AS count FROM notification WHERE user_id=? AND is_read=0', [user_id], one=True)
    return result['count'] if result else 0
