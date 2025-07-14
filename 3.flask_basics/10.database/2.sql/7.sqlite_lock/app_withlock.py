from flask import Flask, request
import sqlite3
import time
import threading

app = Flask(__name__)
db_lock = threading.Lock()  # 전역 락 객체

# DB 초기화 (users 테이블 생성)
conn = sqlite3.connect("users.db")
conn.execute("CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, count INTEGER)")
conn.execute("INSERT OR IGNORE INTO counter (id, count) VALUES (1, 0)")
conn.commit()
conn.close()

@app.route('/update')
def update():
    with db_lock:  # 락 획득
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT count FROM counter WHERE id = 1")
            value = cursor.fetchone()[0]
            time.sleep(1)  # 일부러 지연
            cursor.execute("UPDATE counter SET count = ? WHERE id = 1", (value + 1,))
            conn.commit()
            return f"업데이트 완료 (lock 적용): {value + 1}"
        except Exception as e:
            return f"에러 발생: {e}"
        finally:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
