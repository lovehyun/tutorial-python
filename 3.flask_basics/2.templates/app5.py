from flask import Flask, render_template

app = Flask(__name__)

# 기존 사용자 목록
existing_users = ['Alice', 'Bob', 'Charlie']

@app.route("/")
@app.route("/<name>")
def user(name=""):
    return render_template("users5.html", name=name, existing_users=existing_users)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
