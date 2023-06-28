from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, This is the main page"

@app.route("/user/<name>")
def user(name):
    return f"Hello, {name}! (String)"

@app.route("/user/<int:age>")
def userage(age):
    return f"Age: {age} (Integer)"

@app.route("/user/<float:weight>")
def userweight(weight):
    return f"Weight: {weight} (Float)"

@app.route("/user/<name>/<int:age>")
def usernameage(name, age):
    return f"Hello, {name}! Age: {age}"

@app.route("/user/<name>/<int:age>/<float:weight>")
def userdetail(name, age, weight):
    return f"Hello, {name}! Age: {age}, Weight: {weight}"

if __name__ == "__main__":
    app.run(debug=True)
