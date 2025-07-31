# curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}'
# curl -X GET http://127.0.0.1:5000/protected -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MTE2NzM5OTl9.6Q2d4kR9RijXW1eEHLZz5B9tvVhCvNG2Ed3Hk-pZk9s"

# pip install pyjwt
from flask import Flask, request, jsonify, render_template
import jwt
import datetime

app = Flask(__name__)

# 임의의 시크릿 키 (실제 운영에서는 더 강력한 보안을 위해 안전한 방식으로 관리)
app.config['SECRET_KEY'] = 'my_secret_key'

# 사용자 리스트: dict - dict 구조는 O(1) 로 lookup 가능
"""
users = {
    'user1': {'password': 'password1', 'user_id': 1},
    'user2': {'password': 'password2', 'user_id': 2}
}
"""

# 사용자 리스트: list of dict
users = [
    {'user_id': 1, 'username': 'user1', 'password': 'password1'},
    {'user_id': 2, 'username': 'user2', 'password': 'password2'},
    {'user_id': 3, 'username': 'user3', 'password': 'password3'}
]

# 메인 페이지를 렌더링하는 라우트
@app.route('/')
def index():
    # return render_template('index.html')
    return render_template('index2.html')

# 로그인 요청을 처리하는 라우트
@app.route('/login', methods=['POST'])
def login():
    # 클라이언트로부터 전달받은 로그인 정보 (JSON 형태로 예상)
    login_data = request.json
    username = login_data.get('username')
    password = login_data.get('password')

    # 방법1. dict 인 경우
    # 유효한 사용자인지 확인
    """
    if username in users and users[username]['password'] == password:
        # 유효한 경우, 토큰 발급
        payload = {
            'user_id': users[username]['user_id'],
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    """
    
    # 방법2. list of lict 인 경우
    # 사용자 탐색
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # JWT 발급
    payload = {
        'user_id': user['user_id'],
        'username': user['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

# 토큰이 필요한 보호된 리소스에 접근하는 라우트
@app.route('/protected', methods=['GET'])
def protected_resource():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
        username = decoded_token['username']
        return jsonify({'message': f'Protected resource for user ID {user_id}, {username}'}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)
