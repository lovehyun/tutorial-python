from flask import Flask, request, jsonify
import database4 as db

app = Flask(__name__, static_folder="public", static_url_path="")
app.teardown_appcontext(db.close_db)

@app.route("/")
def home():
    return app.send_static_file("index_restapi.html")

# 전체 조회
@app.route("/api/todo", methods=["GET"])
def get_todos():
    return jsonify(db.get_all_todos())

# 항목 추가
@app.route("/api/todo", methods=["POST"])
def add_todo():
    data = request.get_json(silent=True) or {}
    task = data.get("task", "").strip()
    if not task:
        return jsonify({"error": "Task is required"}), 400
    return jsonify(db.add_todo(task)), 201

# 완료 토글
@app.route("/api/todo/<int:todo_id>", methods=["PUT"])
def toggle_todo(todo_id):
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(db.toggle_todo_status(todo_id))

# 항목 삭제
@app.route("/api/todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.delete_todo(todo_id)
    return jsonify({"message": "Todo deleted successfully"})

if __name__ == "__main__":
    with app.app_context():
        db.init_db()
    app.run(debug=True)
