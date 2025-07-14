import sqlite3

conn = sqlite3.connect("balance.db")
conn.execute("CREATE TABLE IF NOT EXISTS account (id INTEGER PRIMARY KEY, balance INTEGER)")
conn.execute("DELETE FROM account")  # 항상 초기화
conn.execute("INSERT INTO account (id, balance) VALUES (1, 100000)")
conn.commit()
conn.close()

print("잔고를 10만원으로 초기화했습니다.")
