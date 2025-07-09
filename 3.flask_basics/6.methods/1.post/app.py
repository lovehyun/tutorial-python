from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        return redirect(url_for("user", user=user))
    else:
        return render_template("login.html")

@app.route("/user")
@app.route("/user/<user>")
def user(user=None):
        return render_template("user.html", user=user)

@app.route("/product")
def product():
        return render_template("product.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
