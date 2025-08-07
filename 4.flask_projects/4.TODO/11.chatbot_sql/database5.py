# database.py
import sqlite3
from flask import g

DB_PATH = "todos.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL;")
        g.db.execute("PRAGMA foreign_keys=ON;")
    return g.db

def close_db(_exc=None):
    db = g.pop("db", None)
    if db:
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

def row_to_dict(row: sqlite3.Row):
    return {
        "id": row["id"],
        "task": row["task"],
        "done": bool(row["done"]),
        "created_at": row["created_at"]
    }

# CRUD + 검색
def get_all_todos():
    rows = get_db().execute("SELECT * FROM todos ORDER BY id;").fetchall()
    return [row_to_dict(r) for r in rows]

def add_todo(task: str):
    db = get_db()
    cur = db.execute("INSERT INTO todos (task, done) VALUES (?, 0);", (task,))
    db.commit()
    return row_to_dict(db.execute("SELECT * FROM todos WHERE id = ?;", (cur.lastrowid,)).fetchone())

def get_todo_by_id(todo_id: int):
    row = get_db().execute("SELECT * FROM todos WHERE id = ?;", (todo_id,)).fetchone()
    return row_to_dict(row) if row else None

def toggle_todo(todo_id: int):
    db = get_db()
    db.execute("""
        UPDATE todos
        SET done = (CASE WHEN done = 1 THEN 0 ELSE 1 END)
        WHERE id = ?;
    """, (todo_id,))
    db.commit()
    return get_todo_by_id(todo_id)

def delete_todo(todo_id: int):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?;", (todo_id,))
    db.commit()
    return True

def find_todo_by_text(text: str):
    """완전 일치 → 부분 일치 순으로 검색"""
    db = get_db()
    exact = db.execute("SELECT * FROM todos WHERE task = ? LIMIT 1;", (text,)).fetchone()
    if exact:
        return row_to_dict(exact)
    like = db.execute(
        "SELECT * FROM todos WHERE task LIKE ? ORDER BY id DESC LIMIT 1;",
        (f"%{text}%",)
    ).fetchone()
    return row_to_dict(like) if like else None

def get_summary():
    db = get_db()
    total = db.execute("SELECT COUNT(*) FROM todos;").fetchone()[0]
    done = db.execute("SELECT COUNT(*) FROM todos WHERE done = 1;").fetchone()[0]
    return total, done, total - done
