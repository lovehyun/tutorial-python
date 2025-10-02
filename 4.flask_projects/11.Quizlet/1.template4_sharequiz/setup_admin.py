# setup_admin.py
# 최초 관리자 계정 생성 스크립트

from getpass import getpass
from werkzeug.security import generate_password_hash
from database import get_db_connection, init_database


def ensure_schema():
    # init_database()는 필요한 컬럼 추가도 시도함
    init_database()


def create_admin():
    conn = get_db_connection()
    # 관리자 존재 여부 확인
    existing = conn.execute('SELECT id, username FROM users WHERE is_admin = 1 LIMIT 1').fetchone()
    if existing:
        print(f"관리자 계정이 이미 존재합니다: {existing['username']} (id={existing['id']})")
        conn.close()
        return

    print('\n=== 관리자 계정 생성 ===')
    username = input('관리자 사용자명: ').strip()
    email = input('관리자 이메일: ').strip()
    while True:
        pw1 = getpass('비밀번호: ')
        pw2 = getpass('비밀번호 확인: ')
        if pw1 != pw2:
            print('비밀번호가 일치하지 않습니다. 다시 입력하세요.')
        elif len(pw1) < 6:
            print('비밀번호는 최소 6자 이상이어야 합니다.')
        else:
            break

    password_hash = generate_password_hash(pw1)
    try:
        conn.execute('''
            INSERT INTO users (username, email, password_hash, is_admin)
            VALUES (?, ?, ?, 1)
        ''', (username, email, password_hash))
        conn.commit()
        print('관리자 계정이 생성되었습니다.')
    except Exception as e:
        print('관리자 계정 생성 중 오류:', e)
    finally:
        conn.close()


if __name__ == '__main__':
    ensure_schema()
    create_admin()


