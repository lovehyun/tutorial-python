# 요청	        설명	    HTTP Method	요청 데이터
# /api/todo	    전체 조회	GET	없음
# /api/todo	    항목 추가	POST { "task": "Study Flask" }
# /api/todo	    완료 토글	PUT { "id": 1 }
# /api/todo	    항목 삭제	DELETE { "id": 1 }

# app.py
import sqlite3
from flask import Flask, request, jsonify, g

DB_PATH = "todos.db"

app = Flask(__name__, static_folder="public", static_url_path="")

# ---------- SQLite 유틸 ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        
        # 선택: 동시성/안정성 약간 개선
        g.db.execute("PRAGMA journal_mode=WAL;") # Write-Ahead Logging
        g.db.execute("PRAGMA foreign_keys=ON;") # 외래 키 제약 조건 활성화
    return g.db

@app.teardown_appcontext
def close_db(_exc):
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

def row_to_dict(row: sqlite3.Row):
    return {
        "id": row["id"],
        "task": row["task"],
        "done": bool(row["done"]),
        "created_at": row["created_at"]
    }

# ---------- 라우트 ----------
@app.route("/")
def home():
    return app.send_static_file("index_restapi.html")

# 전체 조회
@app.route("/api/todo", methods=["GET"])
def get_todos():
    db = get_db()
    rows = db.execute("SELECT id, task, done, created_at FROM todos ORDER BY id;").fetchall()
    return jsonify([row_to_dict(r) for r in rows])

# 항목 추가
@app.route("/api/todo", methods=["POST"])
def add_todo():
    data = request.get_json(silent=True) or {}  # get_json(silent=True)   # 실패 시 None
                                                # get_json(silent=False)  # 실패 시 에러 발생
    task = data.get("task", "").strip()
    if not task:
        return jsonify({"error": "Task is required"}), 400

    db = get_db()
    cur = db.execute("INSERT INTO todos (task, done) VALUES (?, 0);", (task,))
    db.commit()
    
    new_id = cur.lastrowid
    row = db.execute("SELECT id, task, done, created_at FROM todos WHERE id = ?;", (new_id,)).fetchone()
    return jsonify(row_to_dict(row)), 201

# 완료 토글 (URL 파라미터 사용; 요청 바디 필요 없음)
@app.route("/api/todo/<int:todo_id>", methods=["PUT"])
def toggle_todo(todo_id):
    db = get_db()
    # 존재 여부 체크
    row = db.execute("SELECT id, task, done, created_at FROM todos WHERE id = ?;", (todo_id,)).fetchone()
    if not row:
        return jsonify({"error": "Todo not found"}), 404

    db.execute("UPDATE todos SET done = CASE done WHEN 1 THEN 0 ELSE 1 END WHERE id = ?;", (todo_id,))
    db.commit()
    updated = db.execute("SELECT id, task, done, created_at FROM todos WHERE id = ?;", (todo_id,)).fetchone()
    return jsonify(row_to_dict(updated))

# 항목 삭제
@app.route("/api/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db = get_db()
    # 존재 여부 체크
    row = db.execute("SELECT id FROM todos WHERE id = ?;", (todo_id,)).fetchone()
    if not row:
        return jsonify({"error": "Todo not found"}), 404

    db.execute("DELETE FROM todos WHERE id = ?;", (todo_id,))
    db.commit()
    return jsonify({"message": "Todo deleted successfully"})

# ---------- 실행 ----------
if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
