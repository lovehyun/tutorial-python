from flask import Flask, request, jsonify

app = Flask(__name__)

# 샘플 데이터
users = [
    {'id': 1, 'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'id': 2, 'name': 'Alice', 'age': 30, 'phone': '123-654-4321'},
    {'id': 3, 'name': 'Bob', 'age': 30, 'phone': '987-654-3210'},
    {'id': 4, 'name': 'Charlie', 'age': 35, 'phone': '555-123-4567'}
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

@app.route('/search2')
def search_user2():
    name_query = request.args.get('name')
    age_query = request.args.get('age')
    phone_query = request.args.get('phone')

    results = users

    if name_query:
        results = [user for user in results if name_query.lower() in user['name'].lower()]

    if age_query:
        try:
            age_query = int(age_query)
            results = [user for user in results if user['age'] == age_query]
        except ValueError:
            return jsonify({'error': 'Age parameter must be an integer'}), 400

    if phone_query:
        if len(phone_query) == 4 and phone_query.isdigit():
            results = [user for user in results if user['phone'][-4:] == phone_query]
        else:
            return jsonify({'error': 'Phone parameter must be the last 4 digits'}), 400
            # 한글 깨짐 이슈 해결법
            # return json.dumps({'error': '전화번호는 4자리 숫자로 입력해야 합니다.'}, ensure_ascii=False, indent=4)

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
