import sqlite3

# 데이터베이스 연결 함수
def connect_db():
    return sqlite3.connect('example.db')

# 테이블 생성 함수
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 데이터 삽입 함수
def insert_user(name, age):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()

# 데이터 조회 함수
def get_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall() # 모두
    conn.close()
    return rows

def get_user_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cur.fetchone() # 하나만
    conn.close()
    return user

# 데이터 업데이트 함수
def update_user(name, new_age):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE users SET age = ? WHERE name = ?', (new_age, name))
    conn.commit()
    conn.close()

# 데이터 삭제 함수
def delete_user_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    conn.close()
    
def delete_user_by_id(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# 메인 함수
def main():
    # 테이블 생성
    create_table()
    
    # 데이터 삽입
    insert_user('Alice', 30)
    insert_user('Bob', 25)
    insert_user('Charlie', 35)

    # 데이터 조회
    print("Initial data:")
    users = get_users()
    for user in users:
        print(user)

    # 데이터 업데이트
    update_user('Alice', 32)
    
    # 업데이트 후 데이터 조회
    print("\nAfter updating Alice's age:")
    user = get_user_by_name('Alice')
    print(user)
    
    print('---')
    users = get_users()
    for user in users:
        print(user)

    # 데이터 삭제
    delete_user_by_name('Bob')
    
    # 삭제 후 데이터 조회
    print("\nAfter deleting Bob:")
    user = get_user_by_name('Bob')
    print(user)
    
    print('---')
    users = get_users()
    for user in users:
        print(user)
        
    print("\nAfter deleting others...:")
    delete_user_by_id(1)
    delete_user_by_id(3)
    
    users = get_users()
    for user in users:
        print(user)

if __name__ == '__main__':
    main()
