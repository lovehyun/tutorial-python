import sqlite3
from flask import g

DB_PATH = "todos.db"

# ----------------- 공통 -----------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL;")
        g.db.execute("PRAGMA foreign_keys=ON;")
    return g.db

def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()

def row_to_dict(row):
    return {
        "id": row["id"],
        "task": row["task"],
        "done": bool(row["done"]),
        "created_at": row["created_at"]
    }

# ----------------- CRUD 함수 -----------------
def get_all_todos():
    db = get_db()
    rows = db.execute("SELECT * FROM todos ORDER BY id;").fetchall()
    return [row_to_dict(r) for r in rows]

def get_todo_by_id(todo_id):
    db = get_db()
    row = db.execute("SELECT * FROM todos WHERE id = ?;", (todo_id,)).fetchone()
    return row_to_dict(row) if row else None

def add_todo(task):
    db = get_db()
    cur = db.execute("INSERT INTO todos (task, done) VALUES (?, 0);", (task,))
    db.commit()
    return get_todo_by_id(cur.lastrowid)

def toggle_todo_status(todo_id):
    db = get_db()
    # db.execute("UPDATE todos SET done = 1 - done WHERE id = ?") # toogle 의 단순한 버전
    db.execute("""
        UPDATE todos
        SET done = (
            CASE 
                WHEN done = 1 THEN 0
                ELSE 1
            END
        )
        WHERE id = ?;
    """, (todo_id,))
    db.commit()
    return get_todo_by_id(todo_id)

def delete_todo(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?;", (todo_id,))
    db.commit()
    return True
