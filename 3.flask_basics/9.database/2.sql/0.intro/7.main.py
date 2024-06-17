import db_crud as db

def main():
    # 테이블 생성
    db.create_table()
    
    # 데이터 삽입
    db.insert_user('Alice', 30)
    db.insert_user('Bob', 25)
    db.insert_user('Charlie', 35)

    # 데이터 조회
    print("Initial data:")
    users = db.fetch_users()
    for user in users:
        print(user)

    # 데이터 업데이트
    db.update_user('Alice', 32)
    
    # 업데이트 후 데이터 조회
    print("\nAfter updating Alice's age:")
    users = db.fetch_users()
    for user in users:
        print(user)

    # 데이터 삭제
    db.delete_user('Bob')
    
    # 삭제 후 데이터 조회
    print("\nAfter deleting Bob:")
    users = db.fetch_users()
    for user in users:
        print(user)

if __name__ == '__main__':
    main()
