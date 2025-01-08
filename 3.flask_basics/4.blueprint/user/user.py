from flask import Blueprint, render_template

user_app = Blueprint("user", __name__, static_folder="static", template_folder="../templates/user")

@user_app.route("/")
def home():
    return render_template("index.html")
