from database import model
from flask import Blueprint, redirect, render_template


blueprint = Blueprint('order', __name__, template_folder='./templates')


@blueprint.route('/orders/', defaults={'page_num': 1})
@blueprint.route('/orders/<int:page_num>')
def orders(page_num=1):
    orders = model.Order.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("orders.html", pagination=orders)


@blueprint.route('/order_detail/<order_id>')
def order_detail(order_id):
    order = model.Order.query.filter_by(id=order_id).first()
    if not order:
        return redirect('/orders')

    return render_template("order_detail.html", order=order)


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


@blueprint.route('/items/', defaults={'page_num': 1})
@blueprint.route('/items/<int:page_num>')
def items(page_num=1):
    items = model.Item.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("items.html", pagination=items)


@blueprint.route('/item_detail/<item_id>')
def item_detail(item_id):
    item = model.Item.query.filter_by(id=item_id).first()
    if not item:
        return redirect('/items')

    return render_template("item_detail.html", item=item)
