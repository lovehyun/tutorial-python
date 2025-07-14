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

    users = db.get_users_per_page(page, items_per_page)
    fieldnames = users[0].keys() if users else []  # Row 객체에서도 key 가능

    return render_template('index2.html', data=users, fieldnames=fieldnames,
                           page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
