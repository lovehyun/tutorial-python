# 모든 사용자 보기: http://127.0.0.1:5000/
# Alice 사용자 검색: http://127.0.0.1:5000/user/Alice
# Bob 사용자 검색: http://127.0.0.1:5000/user/Bob

from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'name': 'Bob', 'age': 30, 'phone': '987-654-3210'},
    {'name': 'Charlie', 'age': 35, 'phone': '555-123-4567'}
]

@app.route('/')
def index():
    return jsonify(users)

@app.route('/user/<name>')
def get_user_by_name(name):
    # 이름이 일치하는 사용자 필터링
    user = None
    for u in users:
        if u['name'].lower() == name.lower():
            user = u
            break

        # 나이로도 검색하기
        # if str(u['age']) == name:
        #     user = u
        #     break
    
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
