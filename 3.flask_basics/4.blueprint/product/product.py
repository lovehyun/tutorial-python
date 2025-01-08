from flask import Blueprint, render_template

product_app = Blueprint("product", __name__, static_folder="static", template_folder="../templates/product")

@product_app.route("/")
def home():
    return render_template("index.html")

@product_app.route("/fruit")
def fruit():
    return render_template("fruit.html")

@product_app.route("/drink")
def drink():
    return render_template("drink.html")
