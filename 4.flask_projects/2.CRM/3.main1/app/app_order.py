from flask import Blueprint, render_template

from database.model import Order, OrderItem

blueprint = Blueprint('order', __name__)


@blueprint.route('/orders/', defaults={'page_num': 1})
@blueprint.route('/orders/<int:page_num>')
def orders(page_num=1):
    per_page = 20
    offset = (page_num - 1) * per_page

    # Order 객체 생성
    order = Order()
    orders = order.execute_query(f"SELECT * FROM orders LIMIT {per_page} OFFSET {offset}", fetchall=True)

    return render_template("orders.html", pagination=orders)


@blueprint.route('/order_items/', defaults={'page_num': 1})
@blueprint.route('/order_items/<int:page_num>')
def order_items(page_num=1):
    per_page = 20
    offset = (page_num - 1) * per_page

    # OrderItem 객체 생성
    order_item = OrderItem()
    order_items = order_item.execute_query(f"SELECT * FROM order_items LIMIT {per_page} OFFSET {offset}", fetchall=True)

    return render_template("order_items.html", pagination=order_items)
