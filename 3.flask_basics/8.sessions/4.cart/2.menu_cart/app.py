from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5) # 영구 세션의 유지 시간 설정
# app.permanent_session_lifetime = timedelta(days=7)

users = [
    {'name': 'MyName', 'id': 'user', 'pw': 'password'},
]

items = [
    {'id': 'P001', 'name': 'apple', 'price': 1000},
    {'id': 'P002', 'name': 'banana', 'price': 2000},
    {'id': 'P003', 'name': 'cherry', 'price': 3000},
]

@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
        return render_template("index.html", user=user)

    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        input_id = request.form["id"] # request.form.get('id')
        input_pw = request.form["password"] # request.form.get('password')

        user = next((u for u in users if u["id"] == input_id and u["pw"] == input_pw), None)
        if user:
            session.permanent = True # 영구 세션으로 설정
            session["user"] = user["name"]  # name만 저장 (또는 필요 시 전체 user 객체 저장)
            return redirect(url_for("user"))
        else:
            return render_template("login.html", error="아이디 또는 비밀번호가 틀렸습니다.")
    else: # GET
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))

@app.route("/product")
def product():
    user = session.get("user", None)

    return render_template("product2.html", user=user, items=items)

@app.route("/cart")
def view_cart():
    user = session.get("user")
    if not user:
        return render_template("cart2.html", user=None, items=items, error="로그인 후 이용 가능합니다.")

    cart = session.get("cart", {})
    cart_items = []

    for item_id, item_qty in cart.items():
        item = next((i for i in items if i["id"] == item_id), None)
        if item:
            item_copy = item.copy()
            item_copy["qty"] = item_qty
            item_copy["total"] = item["price"] * item_qty
            cart_items.append(item_copy)

    return render_template("cart2.html", user=user, cart=cart_items)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    user = session.get("user")
    if not user:
        return render_template("product2.html", user=None, items=items, error="로그인 후 이용 가능합니다.")

    item_id = request.form.get("item_id")

    # 장바구니 딕셔너리 초기화
    if "cart" not in session:
        session["cart"] = {}

    # 상품 ID를 장바구니에 추가
    cart = session["cart"]
    
    # 수량 증가 또는 새로 추가
    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    session["cart"] = cart

    # return redirect(url_for("product"))
    return render_template("product2.html", user=user, items=items, message=f"{item_id} 상품이 장바구니에 담겼습니다.")

@app.route("/remove_item_from_cart", methods=["POST"])
def remove_item_from_cart():
    user = session.get("user")
    if not user:
        return render_template("product2.html", user=None, items=items, error="로그인 후 이용 가능합니다.")

    item_id = request.form.get("item_id")
    cart = session.get("cart", {})

    if item_id in cart:
        del cart[item_id]  # 수량 관계없이 통째로 삭제
        session["cart"] = cart
        
        # cart_items로 변환
        cart_items = []
        for item_id, item_qty in cart.items():
            item = next((i for i in items if i["id"] == item_id), None)
            if item:
                item_copy = item.copy()
                item_copy["qty"] = item_qty
                item_copy["total"] = item["price"] * item_qty
                cart_items.append(item_copy)
                
        # return redirect(url_for("view_cart"))  # 메시지는 템플릿에서 처리할 수 있음
        return render_template("cart2.html", user=user, cart=cart_items, message=f"{item_id} 상품이 제거되었습니다.")
    else:
        # cart_items 재구성
        cart_items = []
        for cid, qty in cart.items():
            item = next((i for i in items if i["id"] == cid), None)
            if item:
                item_copy = item.copy()
                item_copy["qty"] = qty
                item_copy["total"] = item["price"] * qty
                cart_items.append(item_copy)

        return render_template("cart2.html", user=user, cart=cart_items, error="장바구니에 해당 상품이 없습니다.")

@app.route("/clear_cart", methods=["POST"])
def clear_cart():
    user = session.get("user")
    if not user:
        return render_template("cart2.html", user=None, items=items, error="로그인 후 이용 가능합니다.")

    session["cart"] = []
    return render_template("cart2.html", user=user, items=items, message="장바구니가 비워졌습니다.")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
