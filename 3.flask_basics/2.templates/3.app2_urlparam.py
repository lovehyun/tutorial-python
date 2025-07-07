from flask import Flask, render_template

app = Flask(__name__)

# 더미 유저 100명 생성
users = [
    {'id': i, 'name': f'User{i}', 'age': 20 + i % 10, 'phone': f'010-0000-{str(i).zfill(4)}'}
    for i in range(1, 101)
]

@app.route('/')
def index():
    # 페이지 요청 없으면 전체 출력
    return render_template('users_query.html', users=users, page=None)

# http://localhost:5000/pages/1
@app.route('/pages/<int:page>')
def paginate(page):
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    paginated_users = users[start:end]

    return render_template('users_query2.html', users=paginated_users, page=page)

if __name__ == '__main__':
    app.run(debug=True)
