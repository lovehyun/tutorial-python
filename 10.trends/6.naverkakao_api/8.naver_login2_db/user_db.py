import sqlite3

DB_PATH = 'users.db'

def get_user_by_naver_id(naver_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE naver_id = ?", (naver_id,))
    user = cur.fetchone()
    conn.close()
    return user

def save_user_if_not_exists(profile):
    user = get_user_by_naver_id(profile["id"])
    if user:
        return user  # 이미 존재
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (naver_id, name, email, profile_image) VALUES (?, ?, ?, ?)",
        (
            profile["id"],
            profile.get("name"),
            profile.get("email"),
            profile.get("profile_image")
        )
    )
    conn.commit()
    conn.close()
    return get_user_by_naver_id(profile["id"])

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naver_id TEXT UNIQUE NOT NULL,
            name TEXT,
            email TEXT,
            profile_image TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("사용자 테이블이 초기화되었습니다.")

if __name__ == '__main__':
    init_db()
