from flask import Flask, request, session, jsonify, send_from_directory

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션 암호화를 위한 키 설정

# 사용자 목록
users = [
    {'name': 'Alice', 'id': 'alice', 'pw': 'alice'},
    {'name': 'Bob', 'id': 'bob', 'pw': 'bob1234'},
    {'name': 'Charlie', 'id': 'charlie', 'pw': 'hello'},
]

@app.route('/')
def home():
    return send_from_directory('static', 'index4.html')

@app.route('/profile')
def profile():
    return send_from_directory('static', 'profile4.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    id = data.get('id')
    pw = data.get('password')

    user = next((user for user in users if user['id'] == id and user['pw'] == pw), None)

    if user:
        session['user'] = user  # 로그인한 사용자 정보를 세션에 저장
        return jsonify({'status': 'success', 'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid ID or password'}), 401

@app.route('/api/profile', methods=['GET', 'POST'])
def api_profile():
    user = session.get('user')
    if not user:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

    if request.method == 'POST':
        data = request.json
        new_password = data.get('new_password')
        for u in users:
            if u['id'] == user['id']:
                u['pw'] = new_password  # 사용자 목록에서 비밀번호 업데이트
                break

        user['pw'] = new_password  # 세션에서 비밀번호 업데이트
        session['user'] = user  # 업데이트된 사용자 정보를 세션에 저장
        return jsonify({'status': 'success', 'message': 'Password successfully updated'}), 200

    return jsonify({'status': 'success', 'user': user}), 200

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user', None)  # 세션에서 사용자 정보 삭제
    return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)
