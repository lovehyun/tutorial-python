from flask import Blueprint, render_template

product_app = Blueprint("product", __name__, static_folder="static", template_folder="templates")

@product_app.route("/")
def home():
    return render_template("product/index.html")

@product_app.route("/fruit")
def fruit():
    return render_template("product/fruit.html")

@product_app.route("/drink")
def drink():
    return render_template("product/drink.html")
