import sqlite3

DB_PATH = 'database.db'  # DB 파일 경로

# 공통 함수 - 커넥션 생성
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Row 객체를 dict처럼 사용 가능하게 설정
    return conn

# 전체 사용자 수 조회 (페이징 계산용)
def get_user_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_user_count_by_name(search_name=""):
    conn = get_connection()
    cursor = conn.cursor()
    if search_name:
        cursor.execute("SELECT COUNT(*) FROM users WHERE Name LIKE ?", ('%' + search_name + '%',))
    else:
        cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# 페이징 처리된 사용자 목록 조회
def get_users_per_page(page, items_per_page):
    offset = (page - 1) * items_per_page
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users LIMIT ? OFFSET ?', (items_per_page, offset))
    rows = cursor.fetchall()
    conn.close()
    return rows  # sqlite3.Row 객체 리스트 반환

def get_users_by_name_per_page(page, per_page, search_name=""):
    offset = (page - 1) * per_page
    conn = get_connection()
    cursor = conn.cursor()
    if search_name:
        cursor.execute("""
            SELECT * FROM users
            WHERE Name LIKE ?
            ORDER BY Id
            LIMIT ? OFFSET ?
        """, ('%' + search_name + '%', per_page, offset))
    else:
        cursor.execute("""
            SELECT * FROM users
            ORDER BY Id
            LIMIT ? OFFSET ?
        """, (per_page, offset))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# 개별 사용자 상세 조회
def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE Id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row  # sqlite3.Row 객체 반환

def get_monthly_revenue():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            substr(o.OrderAt, 1, 7) as Month,
            SUM(CAST(i.UnitPrice AS INTEGER)) as Revenue
        FROM orders o
        JOIN orderitems oi ON o.Id = oi.OrderId
        JOIN items i ON oi.ItemId = i.Id
        GROUP BY Month
        ORDER BY Month
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # rows = [('2023-01', 50000), ('2023-02', 75000), ...]
    labels = [row[0] for row in rows]
    values = [row[1] for row in rows]

    return {'labels': labels, 'values': values}
