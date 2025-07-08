from flask import Blueprint, render_template

product_bp = Blueprint("product", __name__, static_folder="static", template_folder="../templates/product")

@product_bp.route("/")
def home():
    return render_template("index.html")

@product_bp.route("/fruit")
def fruit():
    return render_template("fruit.html")

@product_bp.route("/drink")
def drink():
    return render_template("drink.html")
