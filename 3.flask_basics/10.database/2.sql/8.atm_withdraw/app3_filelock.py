# http://127.0.0.1:5000/withdraw?amount=10000

# pip install filelock

from flask import Flask, request
import sqlite3
import time
from filelock import FileLock, Timeout

app = Flask(__name__)

LOCK_PATH = "balance.db.lock"

@app.route('/withdraw')
def withdraw():
    try:
        amount = int(request.args.get("amount", 0))
    except ValueError:
        return "잘못된 출금 금액입니다."

    if amount <= 0:
        return "출금 금액은 1원 이상이어야 합니다."

    lock = FileLock(LOCK_PATH, timeout=5)  # 5초 이상 대기 시 실패
    print("[LOCK] 파일 락 요청 대기 중...")

    try:
        with lock:  # 파일 락 획득
            print("[LOCK] 파일 락 획득 완료")
            conn = sqlite3.connect("balance.db")
            cursor = conn.cursor()

            cursor.execute("SELECT balance FROM account WHERE id = 1")
            balance = cursor.fetchone()[0]

            time.sleep(1)  # 일부러 지연

            if balance >= amount:
                new_balance = balance - amount
                cursor.execute("UPDATE account SET balance = ? WHERE id = 1", (new_balance,))
                conn.commit()
                return f"출금 성공: {amount}원 → 잔고: {new_balance}원"
            else:
                return f"출금 실패: 잔고({balance}원) 부족"
        
        # 여기 도달하면 락 자동 해제된 시점
        print("[LOCK] 파일 락 해제 완료")
    except Timeout:
        return "다른 작업 중입니다. 잠시 후 다시 시도해주세요."
    except Exception as e:
        return f"에러 발생: {e}"
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
