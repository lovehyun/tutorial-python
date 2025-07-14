import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서 객체 생성
cur = conn.cursor()

# 테이블에 데이터가 있는지 확인하는 쿼리 실행
cur.execute('SELECT COUNT(*) FROM users')
count = cur.fetchone()[0]

# 데이터가 없는 경우에만 데이터 삽입
if count == 0:
    cur.execute('''
        INSERT INTO users (name, age) VALUES (?, ?)
    ''', ('Alice', 30))

    cur.execute('''
        INSERT INTO users (name, age) VALUES (?, ?)
    ''', ('Bob', 25))

    # 커밋하여 변경사항 저장
    conn.commit()
else:
    print('테이블에 이미 데이터가 있습니다.')

# 데이터베이스 연결 닫기
conn.close()
