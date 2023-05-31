from database import model
from flask import Blueprint, redirect, render_template


blueprint = Blueprint('item', __name__)


@blueprint.route('/items/', defaults={'page_num': 1})
@blueprint.route('/items/<int:page_num>')
def items(page_num=1):
    items = model.Item.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("items.html", pagination=items)
