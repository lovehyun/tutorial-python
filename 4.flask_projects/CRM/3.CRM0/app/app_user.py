from flask import Blueprint, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField

from database.model import User

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
    query = "SELECT * FROM users WHERE 1=1"
    if name:
        query += f" AND name LIKE '{name}%'"
    if gender:
        query += f" AND gender = '{gender}'"

    # 쿼리문 실행 .all 또는 .paginate
    per_page = 20
    offset = (page_num - 1) * per_page
    count_query = query
    query += f" LIMIT {per_page} OFFSET {offset}"

    # Model 인스턴스 생성
    user = User()
    users = user.execute_query(query, fetchall=True)
    print(users)
    users_count = len(user.execute_query(count_query, fetchall=True))

    # 조건문이 폼에 계속 유지되도록 쿼리문 재 전달
    query_params = {'name': name, 'gender': gender}

    return render_template("users.html", pagination=users, total_count=users_count, form=form, query=query_params)


@blueprint.route('/user_detail/<user_id>')
def user_detail(user_id):
    # Model 인스턴스 생성
    user = User()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = user.execute_query(query, fetchall=True)

    if result:
        user_data = result[0]
        return render_template("user_detail.html", user=user_data)
    else:
        return redirect('/users')
