from flask import Flask, render_template
import database as db

app = Flask(__name__)

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 10  # 한 페이지에 보여줄 사용자 수

    # 총 사용자 수 가져오기
    total_users = db.get_user_count()

    # 전체 페이지 수 계산
    total_pages = (total_users + per_page - 1) // per_page

    # 현재 페이지 데이터 가져오기
    users = db.get_users_per_page(page, per_page)

    return render_template('index.html', data=users, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
