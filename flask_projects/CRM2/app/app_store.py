from database import model
from flask import Blueprint, redirect, render_template, request
from sqlalchemy.sql.functions import func, sum as sqlsum


blueprint = Blueprint('store', __name__)


@blueprint.route('/stores/', defaults={'page_num': 1})
@blueprint.route('/stores/<int:page_num>')
def stores(page_num=1):
    stores = model.Store.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("stores.html", pagination=stores)


@blueprint.route('/store_detail/<store_id>', methods=['GET'])
def store_detail(store_id):
    store = model.Store.query.filter_by(id=store_id).first()
    if not store:
        return redirect('/stores')
    
    rev_month = request.args.get('rev_month')

    expr = model.Order.storeid == store_id
    if rev_month is None:
        month = func.substr(model.Order.orderat, 0, 8) # 월 매칭 2023-03-
    else:
        month = func.substr(model.Order.orderat, 0, 11) # 일 매칭 2023-03-01
        expr &= func.substr(model.Order.orderat, 0, 8) == rev_month

    # 월간 매출액
    revenues = model.db.session.query(
        month, sqlsum(model.Item.unitprice), func.count()
    ).join(
        model.OrderItem, model.OrderItem.itemid == model.Item.id
    ).join(
        model.Order, model.Order.id == model.OrderItem.orderid
    ).filter(
        expr
    ).group_by(
        month
    ).order_by(
        month
    )

    return render_template("store_detail.html", store=store, revenues=revenues)
