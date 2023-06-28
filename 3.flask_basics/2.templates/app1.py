from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/<name>")
def user(name=""):
    return render_template("index.html", name=name, content=["bill", "steve", "larry"])

if __name__ == "__main__":
    app.run(port=5000, debug=True)
