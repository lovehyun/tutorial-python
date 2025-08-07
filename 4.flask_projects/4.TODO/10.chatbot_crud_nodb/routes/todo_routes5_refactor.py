# routes/todo_routes.py
from flask import Blueprint, request, jsonify
from services import todo_service as svc

todo_bp = Blueprint("todo", __name__)

@todo_bp.route("", methods=["GET"])
@todo_bp.route("/", methods=["GET"])
def get_todos():
    return jsonify(svc.get_all())

@todo_bp.route("", methods=["POST"])
@todo_bp.route("/", methods=["POST"])
def add_todo():
    data = request.get_json() or {}
    task = (data.get("task") or "").strip()
    if not task:
        return jsonify({"error": "Task is required"}), 400
    item = svc.add(task)
    return jsonify(item), 201

@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def toggle_todo(todo_id):
    item = svc.toggle(todo_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Todo not found"}), 404

@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    ok = svc.delete(todo_id)
    if ok:
        return jsonify({"message": "Todo deleted successfully"})
    return jsonify({"error": "Todo not found"}), 404
