# migration.py
"""
스키마 마이그레이션 유틸리티

구버전 DB를 최신 스키마로 안전하게 마이그레이션합니다.
현재 마이그레이션 항목:
- quiz_files 테이블에 is_public INTEGER DEFAULT 0 컬럼 추가
- quiz_files 테이블에 shared_by_user_id INTEGER 컬럼 추가
"""

from database import get_db_connection


def _column_exists(conn, table: str, column: str) -> bool:
    cursor = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def run_migrations() -> None:
    """필요한 경우 스키마를 최신 상태로 마이그레이션."""
    conn = get_db_connection()
    try:
        # quiz_files: is_public
        if not _column_exists(conn, 'quiz_files', 'is_public'):
            conn.execute('ALTER TABLE quiz_files ADD COLUMN is_public INTEGER DEFAULT 0')
            conn.commit()

        # quiz_files: shared_by_user_id
        if not _column_exists(conn, 'quiz_files', 'shared_by_user_id'):
            conn.execute('ALTER TABLE quiz_files ADD COLUMN shared_by_user_id INTEGER')
            conn.commit()

        # quiz_files: shared_source_file_id (가져오기 원본 파일 ID)
        if not _column_exists(conn, 'quiz_files', 'shared_source_file_id'):
            conn.execute('ALTER TABLE quiz_files ADD COLUMN shared_source_file_id INTEGER')
            conn.commit()
    finally:
        conn.close()


