from flask import Flask, request, jsonify

app = Flask(__name__)

# 샘플 데이터
users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
]

@app.route('/users')
def get_users():
    return jsonify(users)

@app.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    user = None
    for u in users:
        if u['id'] == user_id:
            user = u
            break
    if user is not None:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

    # 더 간결한 코드
    # user = next((user for user in users if user['id'] == user_id), None)
    # if user is not None:
    #     return jsonify(user)
    # else:
    #     return jsonify({'error': 'User not found'}), 404

@app.route('/search')
def search_user():
    query = request.args.get('name')
    if not query:
        return jsonify({'error': 'Name parameter is required'}), 400
    results = [user for user in users if query.lower() in user['name'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
