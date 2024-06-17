import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서 객체 생성
cur = conn.cursor()

# 데이터 조회
cur.execute('SELECT * FROM users')

# 모든 행 가져오기
rows = cur.fetchall()

# 결과 출력
for row in rows:
    print(row)

# 데이터베이스 연결 닫기
conn.close()
