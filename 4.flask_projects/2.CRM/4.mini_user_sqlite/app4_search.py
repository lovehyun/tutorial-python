from flask import Flask, render_template, request
import database as db 
import math

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    items_per_page = 10

    total_items = db.get_user_count_by_name(search_name)
    total_pages = math.ceil(total_items / items_per_page)
    users = db.get_users_by_name_per_page(page, items_per_page, search_name)

    # 필드 이름은 users에 데이터가 있을 경우 첫 번째 항목의 키를 기준
    fieldnames = ['index'] + list(users[0].keys()) if users else ['index']

    # 인덱스 추가
    start_index = (page - 1) * items_per_page
    for i, user in enumerate(users, start=start_index + 1):
        user['index'] = i

    return render_template(
        'index4.html',
        fieldnames=fieldnames,
        data=users,
        search_name=search_name,
        page=page,
        total_pages=total_pages
    )

@app.route('/user/<id>')
def user_detail(id):
    user = db.get_user_by_id(id)
    if user:
        return render_template('user_detail3.html', user=user)
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
