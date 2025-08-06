from flask import Blueprint, request, jsonify

todo_bp = Blueprint("todo", __name__)

todos = []
next_id = 1

@todo_bp.route("", methods=["GET"])
@todo_bp.route("/", methods=["GET"])
def get_todos():
    return jsonify(todos)

@todo_bp.route("", methods=["POST"])
@todo_bp.route("/", methods=["POST"])
def add_todo():
    global next_id
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task is required"}), 400

    new_todo = {"id": next_id, "task": task, "done": False}
    todos.append(new_todo)
    next_id += 1
    return jsonify(new_todo), 201

@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify({"message": "Todo deleted successfully"})
    return jsonify({"error": "Todo not found"}), 404
