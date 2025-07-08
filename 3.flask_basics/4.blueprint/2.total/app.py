from flask import Flask, render_template
from admin.admin import admin_bp
from user.user import user_bp
from product.product import product_bp

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(product_bp, url_prefix="/product")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
