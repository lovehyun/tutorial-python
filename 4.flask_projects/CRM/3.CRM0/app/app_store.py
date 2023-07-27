from flask import Blueprint, render_template

from database.model import Store

blueprint = Blueprint('store', __name__)


@blueprint.route('/stores/', defaults={'page_num': 1})
@blueprint.route('/stores/<int:page_num>')
def stores(page_num=1):
    per_page = 20
    offset = (page_num - 1) * per_page

    # Store 객체 생성
    store = Store()
    stores = store.execute_query(f"SELECT * FROM stores LIMIT {per_page} OFFSET {offset}", fetchall=True)

    return render_template("stores.html", pagination=stores)
