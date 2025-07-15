from flask import Blueprint, jsonify
from .models import db, User

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "age": u.age} for u in users])
