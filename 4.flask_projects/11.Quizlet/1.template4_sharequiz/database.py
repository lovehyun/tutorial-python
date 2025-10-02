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
            is_public INTEGER DEFAULT 0,
            shared_by_user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # 기존 DB에 컬럼이 없을 경우 안전하게 추가
    def column_exists(table, column):
        cursor.execute(f"PRAGMA table_info({table})")
        return any(row[1] == column for row in cursor.fetchall())

    try:
        # users: is_admin
        if not column_exists('users', 'is_admin'):
            cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
        # users: login_count
        if not column_exists('users', 'login_count'):
            cursor.execute('ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0')
        if not column_exists('quiz_files', 'is_public'):
            cursor.execute('ALTER TABLE quiz_files ADD COLUMN is_public INTEGER DEFAULT 0')
        if not column_exists('quiz_files', 'shared_by_user_id'):
            cursor.execute('ALTER TABLE quiz_files ADD COLUMN shared_by_user_id INTEGER')
        if not column_exists('quiz_files', 'shared_source_file_id'):
            cursor.execute('ALTER TABLE quiz_files ADD COLUMN shared_source_file_id INTEGER')
    except Exception:
        # SQLite 일부 버전에서 ALTER 실패 시 무시 (이미 적용되었을 가능성)
        pass
    
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
    
    # quiz_sessions 테이블 생성 (퀴즈 세션 관리)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_file_id INTEGER NOT NULL,
            session_token VARCHAR(255) UNIQUE NOT NULL,
            questions_data TEXT NOT NULL,
            settings TEXT NOT NULL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_file_id) REFERENCES quiz_files (id) ON DELETE CASCADE
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

def create_quiz_session(user_id, quiz_file_id, questions_data, settings):
    """퀴즈 세션 생성"""
    import uuid
    import json
    from datetime import datetime, timedelta
    
    session_token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(hours=2)  # 2시간 후 만료
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO quiz_sessions 
        (user_id, quiz_file_id, session_token, questions_data, settings, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id, 
        quiz_file_id, 
        session_token, 
        json.dumps(questions_data), 
        json.dumps(settings),
        expires_at
    ))
    conn.commit()
    conn.close()
    
    return session_token

def get_quiz_session(session_token):
    """퀴즈 세션 조회"""
    import json
    from datetime import datetime
    
    conn = get_db_connection()
    session = conn.execute(
        'SELECT * FROM quiz_sessions WHERE session_token = ? AND is_active = 1',
        (session_token,)
    ).fetchone()
    conn.close()
    
    if not session:
        return None
    
    # 만료 시간 확인
    if session['expires_at'] and datetime.fromisoformat(session['expires_at']) < datetime.now():
        return None
    
    # JSON 데이터 파싱
    session_data = {
        'id': session['id'],
        'user_id': session['user_id'],
        'quiz_file_id': session['quiz_file_id'],
        'session_token': session['session_token'],
        'questions_data': json.loads(session['questions_data']),
        'settings': json.loads(session['settings']),
        'started_at': session['started_at'],
        'expires_at': session['expires_at']
    }
    
    return session_data

def deactivate_quiz_session(session_token):
    """퀴즈 세션 비활성화"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE quiz_sessions SET is_active = 0 WHERE session_token = ?',
        (session_token,)
    )
    conn.commit()
    conn.close()

def cleanup_expired_sessions():
    """만료된 세션 정리"""
    from datetime import datetime
    
    conn = get_db_connection()
    conn.execute(
        'UPDATE quiz_sessions SET is_active = 0 WHERE expires_at < ?',
        (datetime.now(),)
    )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
