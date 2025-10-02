# database.py
# SQLite 데이터베이스 초기화 및 테이블 생성

import sqlite3
import os

DB_PATH = 'data/quizlet.db'
UPLOAD_PATH = 'data/uploads'

def init_database():
    """데이터베이스 및 테이블 초기화"""
    # uploads 디렉토리 생성
    os.makedirs(UPLOAD_PATH, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # users 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login_at TIMESTAMP
        )
    ''')
    
    # quiz_files 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            question_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # quiz_results 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_file_id INTEGER NOT NULL,
            score FLOAT NOT NULL,
            total_questions INTEGER NOT NULL,
            correct_answers INTEGER NOT NULL,
            time_taken INTEGER,
            settings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_file_id) REFERENCES quiz_files (id) ON DELETE CASCADE
        )
    ''')
    
    # user_settings 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mode VARCHAR(20) NOT NULL,
            question_order VARCHAR(20) DEFAULT 'original',
            choice_order VARCHAR(20) DEFAULT 'original',
            question_limit INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, mode)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"데이터베이스가 성공적으로 초기화되었습니다: {DB_PATH}")

def get_db_connection():
    """데이터베이스 연결 반환"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
    return conn

def create_user_upload_folder(user_id):
    """사용자별 업로드 폴더 생성"""
    user_folder = f'data/uploads/user_{user_id}'
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

if __name__ == '__main__':
    init_database()
