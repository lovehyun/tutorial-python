# REST API + fetch 방식 예제
# - HTML 은 모두 static 폴더에서 정적으로 서빙
# - 데이터는 /api/... 엔드포인트가 JSON 으로 응답
# - 브라우저에서 fetch 로 호출해서 화면을 그림
#
# 페이지:
# - /            : static/index.html
# - /user        : static/user.html       (URL path param 방식: /api/users/<id>)
# - /product     : static/product.html    (Query param 방식: /api/products?id=...)

from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder="static", static_url_path="")

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


# ---------- 정적 페이지 ----------
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/user")
def user_page():
    return send_from_directory("static", "user.html")


@app.route("/product")
def product_page():
    return send_from_directory("static", "product.html")


# ---------- REST API ----------

# URL path param 방식
@app.route("/api/users")
def api_users():
    return jsonify(list(users.values()))


@app.route("/api/users/<int:user_id>")
def api_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


# Query param 방식 (id, name 중 하나 또는 둘 다 — AND 조건으로 필터)
# - /api/products                    → 전체
# - /api/products?id=101              → id 일치
# - /api/products?name=Lap            → name 부분일치 (대소문자 무시)
# - /api/products?id=101&name=Laptop  → 둘 다 만족
@app.route("/api/products")
def api_products():
    product_id = request.args.get("id", type=int)
    product_name = (request.args.get("name", type=str) or "").strip().lower()

    results = list(products.values())
    if product_id is not None:
        results = [p for p in results if p["id"] == product_id]
    if product_name:
        results = [p for p in results if product_name in p["name"].lower()]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
