from flask import Flask, render_template, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.permanent_session_lifetime = timedelta(days=1)


# 물건의 정보를 딕셔너리로 선언합니다.
items = [
    {'id': 'item1', 'name': '상품1', 'price': 1000},
    {'id': 'item2', 'name': '상품2', 'price': 2000},
    {'id': 'item3', 'name': '상품3', 'price': 3000}
]

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    # 카트가 없으면 새로운 카트를 생성합니다.
    if 'cart' not in session:
        session['cart'] = {}

    # 카트에 물건을 추가하거나 수량을 증가시킵니다.
    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        item = next((item for item in items if item['id'] == item_id), None)
        if item:
            session['cart'][item_id] = 1
    
    # 세션 데이터가 수정되었음을 Flask에 알립니다.
    session.modified = True

    return redirect(url_for('index'))

@app.route('/view_cart')
def view_cart():
    cart_items = {}
    total_price = 0

    # 카트에 담긴 물건들과 수량을 조회합니다.
    for item_id, quantity in session.get('cart', {}).items():
        item = next((item for item in items if item['id'] == item_id), None)
        if item:
            cart_items[item_id] = {
                'name': item['name'], 
                'quantity': quantity, 
                'price': item['price']
            }
            total_price += item['price'] * quantity

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_item_from_cart/<item_id>')
def remove_item_from_cart(item_id):
    # 카트에서 물건을 제거합니다.
    if 'cart' in session and item_id in session['cart']:
        session['cart'].pop(item_id)
        session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/clear_cart')
def clear_cart():
    # 카트를 비웁니다.
    if 'cart' in session:
        session.pop('cart')
    return redirect(url_for('view_cart'))


if __name__ == '__main__':
    app.run(debug=True)
