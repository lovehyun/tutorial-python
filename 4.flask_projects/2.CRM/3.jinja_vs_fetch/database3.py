import sqlite3

DATABASE = 'database/database.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def get_stores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores")
    stores = cursor.fetchall()
    conn.close()
    return stores

def get_store_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores WHERE Name LIKE ?", ('%' + name + '%',))
    stores = cursor.fetchall()
    conn.close()
    return stores
