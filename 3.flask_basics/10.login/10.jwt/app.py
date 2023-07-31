# pip install PyJWT

from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# 임의의 시크릿 키 (실제 운영에서는 더 강력한 보안을 위해 안전한 방식으로 관리)
app.config['SECRET_KEY'] = 'my_secret_key'

# 로그인 정보 (임의로 하드코딩)
users = {
    'user1': {'password': 'password1', 'user_id': 1},
    'user2': {'password': 'password2', 'user_id': 2}
}

# 로그인 요청을 처리하는 라우트
@app.route('/login', methods=['POST'])
def login():
    # 클라이언트로부터 전달받은 로그인 정보 (JSON 형태로 예상)
    login_data = request.json
    username = login_data.get('username')
    password = login_data.get('password')

    # 유효한 사용자인지 확인
    if username in users and users[username]['password'] == password:
        # 유효한 경우, 토큰 발급
        token = jwt.encode({'user_id': users[username]['user_id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# 토큰이 필요한 보호된 리소스에 접근하는 라우트
@app.route('/protected', methods=['GET'])
def protected_resource():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
        return jsonify({'message': f'Protected resource for user ID {user_id}'}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)
