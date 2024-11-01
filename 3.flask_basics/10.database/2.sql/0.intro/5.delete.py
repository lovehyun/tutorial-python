import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')

# 커서 객체 생성
cur = conn.cursor()

# 데이터 삭제
cur.execute('''
    DELETE FROM users WHERE name = ?
''', ('Bob',))

# 커밋하여 변경사항 저장
conn.commit()

# 데이터베이스 연결 닫기
conn.close()
