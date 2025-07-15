import sqlite3

DATABASE = 'database.db'

#--------------------
# 접속
#--------------------
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # 데이터를 행(row) 형태로 반환하도록 설정
    return conn


#--------------------
# 상점 목록 가져오기
#--------------------
def get_stores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = cursor.fetchall()
    conn.close()
    
    stores = [dict(row) for row in stores] # Row 타입을 dict 타입으로 변환
    return stores

# 컬럼명 추출 및 ROWS를 기반으로 수동으로 key 매핑하도록...
def get_stores2():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    rows = cursor.fetchall()

    # 리스트 iterate 하면서 하나씩 key, value 매핑
    stores = []
    for store in rows:
        stores.append({
            'id': store[0],
            'name': store[1],
            'type': store[2],
            'address': store[3]
        })

    # 리스트 컴프리헨션으로 짧게
    stores = [{'id': r[0], 'name': r[1], 'type': r[2], 'address': r[3]} for r in rows]

    conn.close()
    return stores

# 컬럼명 추출 및 ROWS를 기반으로 자동으로 매핑하도록...
def get_stores3():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    columns = [desc[0] for desc in cursor.description] # 컬럼명 추출

    rows  = cursor.fetchall()
    stores = [dict(zip(columns, row)) for row in rows]  # 수동으로 dict 매핑
    
    conn.close()
    return stores


#--------------------
# 상점명 검색
#--------------------
def get_store_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores WHERE Name LIKE ?", ('%' + name + '%',))
    stores = cursor.fetchall()
    conn.close()

    stores = [dict(row) for row in stores] # Row 타입을 dict 타입으로 변환

    return stores
