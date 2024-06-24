import sqlite3

DATABASE = 'database.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 데이터를 행(row) 형태로 반환하도록 설정
    return conn

def get_stores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = cursor.fetchall()
    conn.close()

    stores = [dict(row) for row in stores] # Row 타입을 dict 타입으로 변환

    return stores

def get_store_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores WHERE Name LIKE ?", ('%' + name + '%',))
    stores = cursor.fetchall()
    conn.close()

    stores = [dict(row) for row in stores] # Row 타입을 dict 타입으로 변환

    return stores
