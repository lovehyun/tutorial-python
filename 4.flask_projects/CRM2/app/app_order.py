from database import model
from flask import Blueprint, redirect, render_template


blueprint = Blueprint('order', __name__)


@blueprint.route('/orders/', defaults={'page_num': 1})
@blueprint.route('/orders/<int:page_num>')
def orders(page_num=1):
    orders = model.Order.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("orders.html", pagination=orders)


@blueprint.route('/order_detail/<order_id>')
def order_detail(order_id):
    orders = model.Order.query.filter_by(id=order_id).all()
    if not orders:
        return redirect('/orders')

    return render_template("order_detail.html", orders=orders)


@blueprint.route('/order_items/', defaults={'page_num': 1})
@blueprint.route('/order_items/<int:page_num>')
def order_items(page_num=1):
    order_items = model.OrderItem.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("order_items.html", pagination=order_items)


@blueprint.route('/orderitem_detail/<order_id>')
def orderitem_detail(order_id):
    orderitems = model.OrderItem.query.filter_by(orderid=order_id).all()
    if not orderitems:
        return redirect('/orders')
    
    return render_template("orderitem_detail.html", orderitems=orderitems)
