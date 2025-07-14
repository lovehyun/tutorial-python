from flask import Flask, render_template, request
import math
import database  # 위의 database.py

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    search_name = request.args.get('name', default='', type=str)
    items_per_page = request.args.get('items_per_page', default=10, type=int)

    total_items = database.get_user_count_by_name(search_name)
    total_pages = math.ceil(total_items / items_per_page)
    users = database.get_users_by_name_per_page(page, items_per_page, search_name)

    # 각 사용자에 인덱스 부여
    for i, user in enumerate(users, start=(page - 1) * items_per_page + 1):
        user["index"] = i

    fieldnames = ["index"] + [key for key in users[0].keys() if key != "index"] if users else []

    return render_template(
        "index5.html",
        fieldnames=fieldnames,
        data=users,
        search_name=search_name,
        page=page,
        total_pages=total_pages,
        items_per_page=items_per_page
    )

@app.route('/user/<id>')
def user_detail(id):
    user = database.get_user_by_id(id)
    if user:
        return render_template("user_detail3.html", user=user)
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
