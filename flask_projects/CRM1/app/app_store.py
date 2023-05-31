from database import model
from flask import Blueprint, redirect, render_template, request
from sqlalchemy.sql.functions import func, sum as sqlsum


blueprint = Blueprint('store', __name__)


@blueprint.route('/stores/', defaults={'page_num': 1})
@blueprint.route('/stores/<int:page_num>')
def stores(page_num=1):
    stores = model.Store.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("stores.html", pagination=stores)
