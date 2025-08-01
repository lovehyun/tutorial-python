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

def save_user_if_not_exists(profile, address=None, phone=None):
    user = get_user_by_naver_id(profile["id"])
    if user:
        return user

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (naver_id, name, nickname, email, profile_image, address, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        profile["id"],
        profile.get("name"),
        profile.get("nickname"),
        profile.get("email"),
        profile.get("profile_image"),
        address,
        phone
    ))
    conn.commit()
    conn.close()

def update_user_profile(user_id, name, nickname, email, phone, address):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET name = ?, nickname = ?, email = ?, phone = ?, address = ?
        WHERE id = ?
    """, (name, nickname, email, phone, address, user_id))
    conn.commit()
    conn.close()

def delete_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naver_id TEXT UNIQUE NOT NULL,
            name TEXT,
            nickname TEXT,
            email TEXT,
            profile_image TEXT,
            address TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("사용자 테이블이 초기화되었습니다.")

if __name__ == '__main__':
    init_db()
