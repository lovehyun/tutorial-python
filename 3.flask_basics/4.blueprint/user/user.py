from flask import Blueprint, render_template

user_app = Blueprint("user", __name__, static_folder="static", template_folder="templates")

@user_app.route("/")
def home():
    return render_template("user/index.html")
