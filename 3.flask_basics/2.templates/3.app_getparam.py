from flask import Flask, request, render_template

app = Flask(__name__)

# 더미 유저 100명 생성
users = [
    {'id': i, 'name': f'User{i}', 'age': 20 + i % 10, 'phone': f'010-0000-{str(i).zfill(4)}'}
    for i in range(1, 101)
]

# http://localhost:5000/?pages=1
@app.route('/')
def index():
    page = request.args.get('pages', type=int)  # 전달되지 않으면 None
    per_page = 10
    # per_page = request.args.get('count', 10, type=int)  # 페이지당 항목 수, 기본값 10

    if page is None:
        # 페이지 파라미터가 없으면 전체 출력
        paginated_users = users
    else:
        start = (page - 1) * per_page
        end = start + per_page
        paginated_users = users[start:end]

    return render_template('users_query2.html', users=paginated_users, page=page)

if __name__ == '__main__':
    app.run(debug=True)
