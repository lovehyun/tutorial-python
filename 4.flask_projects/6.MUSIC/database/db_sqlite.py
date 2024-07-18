import sqlite3
import os

# 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'music.db')

# SQLite3 데이터베이스 초기화
def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS music (
                            music_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            artist TEXT NOT NULL,
                            album_image TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS comment (
                            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            music_id INTEGER,
                            user_id INTEGER,
                            content TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE,
                            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS likes (
                            user_id INTEGER,
                            music_id INTEGER,
                            liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            PRIMARY KEY (user_id, music_id),
                            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                            FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS notification (
                            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            music_id INTEGER,
                            message TEXT,
                            is_read BOOLEAN DEFAULT FALSE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                            FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE)''')
        conn.commit()

def query_db(query, args=(), one=False):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, args)
        r = cursor.fetchall()
        conn.commit()
        return (r[0] if r else None) if one else r

def execute_db(query, args=()):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

def get_notification_count(user_id):
    result = query_db('SELECT COUNT(*) AS count FROM notification WHERE user_id=? AND is_read=0', [user_id], one=True)
    return result['count'] if result else 0
