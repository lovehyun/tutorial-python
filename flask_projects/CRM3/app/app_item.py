from database import model
from flask import Blueprint, redirect, render_template
from sqlalchemy.sql.functions import func, sum as sqlsum


blueprint = Blueprint('item', __name__)


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

    # 아이템 판매 월별 매출액
    revenues = model.db.session.query(
        func.substr(model.Order.orderat, 0, 8).label('month'),
        sqlsum(model.Item.unitprice).label('total_revenue'),
        func.count().label('item_count')
    ).join(
        model.OrderItem, model.OrderItem.itemid == model.Item.id
    ).join(
        model.Order, model.Order.id == model.OrderItem.orderid
    ).filter(
        model.OrderItem.itemid == item_id
    ).group_by(
        func.substr(model.Order.orderat, 0, 8)
    ).order_by(
        func.substr(model.Order.orderat, 0, 8)
    )

    return render_template("item_detail.html", item=item, revenues=revenues)
