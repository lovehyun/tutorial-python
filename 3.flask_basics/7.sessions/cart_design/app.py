from flask import Flask, render_template, session, redirect, url_for, make_response
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.permanent_session_lifetime = timedelta(days=1)


# 물건의 정보를 딕셔너리로 선언합니다.
items = {
    'item1': {'name': '상품1', 'price': 1000, 'image': 'item1.jpg'},
    'item2': {'name': '상품2', 'price': 2000, 'image': 'item2.jpg'},
    'item3': {'name': '상품3', 'price': 3000, 'image': 'item3.jpg'}
}


@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/add_to_cart/<item_name>')
def add_to_cart(item_name):
    # 카트가 없으면 새로운 카트를 생성합니다.
    if 'cart' not in session:
        session['cart'] = {}

    # 카트에 물건을 추가하거나 수량을 증가시킵니다.
    # session['cart'][item_name] = session['cart'].get(item_name, 0) + 1
    if item_name in session['cart']:
        session['cart'][item_name] += 1
        print(f"상품추가 {item_name}")
    else:
        print("신규상품추가")
        item_info = items.get(item_name)
        if item_info:
            session['cart'][item_name] = 1
    
    # 세션 데이터가 수정되었음을 Flask에 알립니다.
    session.modified = True

    return redirect(url_for('index'))

@app.route('/view_cart')
def view_cart():
    cart_items = {}
    total_price = 0

    # 카트에 담긴 물건들과 수량을 조회합니다.
    for item_name, quantity in session.get('cart', {}).items():
        item_info = items.get(item_name)
        if item_info:
            cart_items[item_name] = {'name': item_info['name'], 'quantity': quantity, 'price': item_info['price'], 'image': item_info['image']}
            total_price += item_info['price'] * quantity

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_item_from_cart/<item_name>')
def remove_item_from_cart(item_name):
    if 'cart' in session and item_name in session['cart']:
        session['cart'].pop(item_name)
        # 세션 데이터가 수정되었음을 Flask에 알립니다.
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/clear_cart')
def clear_cart():
    if 'cart' in session:
        session.pop('cart')
        # 세션 데이터가 수정되었음을 Flask에 알립니다.
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Expire the session cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie('session', '', expires=0)

    return response

if __name__ == '__main__':
    app.run(debug=True)
