import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서 객체 생성
cur = conn.cursor()

# 데이터 업데이트
cur.execute('''
    UPDATE users SET age = ? WHERE name = ?
''', (35, 'Alice'))

# 커밋하여 변경사항 저장
conn.commit()

# 데이터베이스 연결 닫기
conn.close()
