# http://127.0.0.1:5000/withdraw?amount=10000

from flask import Flask, request
import sqlite3
import time

app = Flask(__name__)

@app.route('/withdraw')
def withdraw():
    try:
        amount = int(request.args.get("amount", 0))
    except ValueError:
        return "잘못된 출금 금액입니다."

    if amount <= 0:
        return "출금 금액은 1원 이상이어야 합니다."

    conn = sqlite3.connect("balance.db")
    try:
        # 트랜잭션 시작: 쓰기 락 확보
        conn.isolation_level = None             # 수동 트랜잭션
        conn.execute("BEGIN IMMEDIATE")         # 즉시 쓰기 락 (다른 쓰기 차단)

        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM account WHERE id = 1")
        balance = cursor.fetchone()[0]

        time.sleep(1)  # 테스트용 지연 → 동시 요청 충돌 유도

        if balance >= amount:
            cursor.execute("UPDATE account SET balance = ? WHERE id = 1", (balance - amount,))
            conn.commit()
            return f"[TX] 출금 성공: {amount}원 → 남은 잔고: {balance - amount}원"
        else:
            conn.rollback()
            return f"[TX] 출금 실패: 잔고({balance}원) 부족"
    except Exception as e:
        conn.rollback()
        return f"[TX] 에러 발생: {e}"
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
