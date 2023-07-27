from flask import Blueprint, render_template

from database.model import Item

blueprint = Blueprint('item', __name__)


@blueprint.route('/items/', defaults={'page_num': 1})
@blueprint.route('/items/<int:page_num>')
def items(page_num=1):
    per_page = 20
    offset = (page_num - 1) * per_page

    # Item 객체 생성
    item = Item()
    items = item.execute_query(f"SELECT * FROM items LIMIT {per_page} OFFSET {offset}", fetchall=True)

    return render_template("items.html", pagination=items)
