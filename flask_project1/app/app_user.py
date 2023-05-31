from database import model
from flask import Blueprint, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, StringField


blueprint = Blueprint('user', __name__)


class ReusableForm(FlaskForm):
    '''
    search field name, gender forms
    '''
    name = StringField('Name:')
    choices = [('', 'ALL'), ('female', 'F'), ('male', 'M')]
    gender = SelectField('Gender:', choices=choices)


@blueprint.route('/users/', defaults={'page_num': 1}, methods=['GET', 'POST'])
@blueprint.route('/users/<int:page_num>', methods=['GET', 'POST'])
def users(page_num):
    form = ReusableForm(request.form)
    name = request.args.get('name', default=None)
    gender = request.args.get('gender', default=None)

    # http method options
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        page_num = 1  # restart search on new query

    # query statement build-up
    users = model.User.query
    if name:
        users = users.filter(model.User.name.like('{}%'.format(name)))
    if gender:
        users = users.filter(model.User.gender.like('{}'.format(gender)))

    # execute query : .all / .paginate
    users = users.paginate(per_page=20, page=page_num, error_out=True)

    query = {'name': name, 'gender': gender}

    return render_template("users.html", pagination=users, form=form, query=query)


@blueprint.route('/user_detail/<user_id>')
def user_detail(user_id):
    user = model.User.query.get(user_id)

    if user is None:
        return redirect('/users')

    userOrders = user.orderR

    return render_template("user_detail.html", user=user, orders=userOrders)
