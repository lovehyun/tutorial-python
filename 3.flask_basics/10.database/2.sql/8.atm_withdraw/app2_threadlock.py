# http://127.0.0.1:5000/withdraw?amount=10000

from flask import Flask, request
import sqlite3
import time
import threading

app = Flask(__name__)

# 전역 락 (옵션: 실험을 위해 주석 처리 가능)
db_lock = threading.Lock()

@app.route('/withdraw')
def withdraw():
    # 1. 출금 금액 파라미터 받기
    try:
        amount = int(request.args.get("amount", 0))
    except ValueError:
        return "잘못된 출금 금액입니다."

    if amount <= 0:
        return "출금 금액은 1원 이상이어야 합니다."

    print("[LOCK] 락 요청 대기 중...")  # 요청 들어옴
    with db_lock:  # 테스트용 락 (원하면 주석 해제)
        print("[LOCK] 락 획득 완료")
        conn = sqlite3.connect("balance.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT balance FROM account WHERE id = 1")
            balance = cursor.fetchone()[0]

            time.sleep(1)  # 일부러 지연 → 동시성 테스트 유도

            if balance >= amount:
                new_balance = balance - amount
                cursor.execute("UPDATE account SET balance = ? WHERE id = 1", (new_balance,))
                conn.commit()
                return f"{amount}원 출금 성공! 남은 잔고: {new_balance}원"
            else:
                return f"출금 실패: 잔고({balance}원) 부족"
        except Exception as e:
            return f"에러 발생: {e}"
        finally:
            conn.close()
            print("[LOCK] 락 해제 완료")  # with 블록 끝 → 자동 릴리즈

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
