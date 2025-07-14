from flask import Flask, render_template, request
import math
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    items_per_page = 10

    total_items = db.get_user_count()
    total_pages = math.ceil(total_items / items_per_page)

    # Row 객체 → dict로 변환
    users_raw = db.get_users_per_page(page, items_per_page)
    users = [dict(user) for user in users_raw]

    # fieldnames는 첫 줄에서 키를 추출
    fieldnames = list(users[0].keys()) if users else []

    return render_template('index3.html',
                           data=users,
                           fieldnames=fieldnames,
                           page=page,
                           total_pages=total_pages)

@app.route('/user/<id>')
def user_detail(id):
    user = db.get_user_by_id(id)
    if user:
        return render_template('user_detail3.html', user=dict(user))
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
