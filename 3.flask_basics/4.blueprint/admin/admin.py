from flask import Blueprint, render_template

admin_app = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin_app.route("/")
def home():
    return render_template("admin/index.html")

@admin_app.route("/test")
def test():
    return "<h1>test</h1>"
