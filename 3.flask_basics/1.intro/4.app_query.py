from flask import Flask, request

app = Flask(__name__)

# 쿼리 매개변수 처리
@app.route('/search')
def search():
    query = request.args.get('q')
    page = request.args.get('page', default=1, type=int)
    return f'Searching for: {query} on page {page}'

@app.route('/user/<username>/posts')
def show_user_posts(username):
    page = request.args.get('page', default=1, type=int)
    return f'User {username}, page {page}'

if __name__ == '__main__':
    app.run(debug=True)
