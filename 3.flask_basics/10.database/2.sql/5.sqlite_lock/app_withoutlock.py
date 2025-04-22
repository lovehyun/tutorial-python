from flask import Flask, request
import sqlite3
import time  # 인위적으로 지연
import threading

app = Flask(__name__)

# DB 초기화 (users 테이블 생성)
conn = sqlite3.connect("users.db")
conn.execute("CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, count INTEGER)")
conn.execute("INSERT OR IGNORE INTO counter (id, count) VALUES (1, 0)")
conn.commit()
conn.close()

@app.route('/update')
def update():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT count FROM counter WHERE id = 1")
        value = cursor.fetchone()[0]
        time.sleep(1)  # 일부러 지연시켜 동시 요청 시 충돌 유도
        cursor.execute("UPDATE counter SET count = ? WHERE id = 1", (value + 1,))
        conn.commit()
        return f"업데이트 완료: {value + 1}"
    except Exception as e:
        return f"에러 발생: {e}"
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
