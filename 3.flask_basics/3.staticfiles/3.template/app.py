# 서버 사이드 렌더링 (Jinja2 Template) 방식 예제
# - /                       : index.html 렌더링
# - /user/<id>              : URL path param 방식으로 사용자 조회
# - /product?id=&name=      : Query param 방식으로 제품 조회 (id, name 중 하나 또는 둘 다)

from flask import Flask, render_template, request

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Alice",   "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob",     "email": "bob@example.com"},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
}

products = {
    101: {"id": 101, "name": "Laptop", "price": 1200},
    102: {"id": 102, "name": "Phone",  "price": 800},
    103: {"id": 103, "name": "Tablet", "price": 500},
}


@app.route("/")
def home():
    return render_template("index.html")


# URL path param 방식: /user, /user/1, /user/2 ...
@app.route("/user")
@app.route("/user/<int:user_id>")
def user(user_id=None):
    return render_template("user.html", user_id=user_id, users=users)


# Query param 방식: /product, /product?id=101, /product?name=Lap, /product?id=101&name=Lap
# id, name 둘 중 하나만 줘도 되고, 둘 다 줘도 됨 (AND 조건)
@app.route("/product")
def product():
    product_id = request.args.get("id", type=int)
    product_name = (request.args.get("name", type=str) or "").strip()

    found = list(products.values())
    if product_id:
        found = [p for p in found if p["id"] == product_id]
    if product_name:
        found = [p for p in found if product_name.lower() in p["name"].lower()]

    return render_template("product.html", results=found)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
