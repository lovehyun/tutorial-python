from database import model
from flask import Blueprint, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField


blueprint = Blueprint('user', __name__)


class MyForm(FlaskForm):
    name = StringField('Name:')
    gender = SelectField('Gender:', choices=[(''), ('female'), ('male')])


@blueprint.route('/users/', defaults={'page_num': 1}, methods=['GET', 'POST'])
@blueprint.route('/users/<int:page_num>', methods=['GET', 'POST'])
def users(page_num):
    form = MyForm(request.form)
    name = request.args.get('name', default='')
    gender = request.args.get('gender', default=None)

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        page_num = 1  # 검색 시 페이징 초기화

    # 쿼리문 빌드업
    users = model.User.query
    if name:
        users = users.filter(model.User.name.like('{}%'.format(name)))
    if gender:
        users = users.filter(model.User.gender.like('{}'.format(gender)))

    # 쿼리문 실행 .all 또는 .paginate
    users = users.paginate(per_page=20, page=page_num, error_out=True)

    # 조건문이 폼에 계속 유지되도록 쿼리문 재 전달
    query = {'name': name, 'gender': gender}

    return render_template("users.html", pagination=users, form=form, query=query)


@blueprint.route('/user_detail/<user_id>')
def user_detail(user_id):
    user = model.User.query.get(user_id)

    if user is None:
        return redirect('/users')

    userOrders = user.orderR

    return render_template("user_detail.html", user=user, orders=userOrders)
