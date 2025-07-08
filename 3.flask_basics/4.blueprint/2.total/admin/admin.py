from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__, static_folder="static", template_folder="../templates/admin")

@admin_bp.route("/")
def home():
    return render_template("index.html")

@admin_bp.route("/test")
def test():
    return "<h1>test</h1>"
