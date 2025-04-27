# pip install bcrypt
from flask import Flask, request, jsonify, session, send_from_directory
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import sqlite3
import os
import bcrypt

app = Flask(__name__)
app.secret_key = 'secret_key'
DATABASE = 'database.db'

login_manager = LoginManager()
login_manager.init_app(app)

# DB 연결
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# User 모델
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        user = conn.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['password'])
        return None

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        user = conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['password'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# API: 회원가입
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': '모든 필드를 입력하세요.'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db()
    try:
        conn.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                     (username, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '이미 존재하는 사용자입니다.'}), 400
    conn.close()
    return jsonify({'message': '회원가입 성공!'})


# API: 로그인
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db()
    user = conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({'error': '이메일 또는 비밀번호가 틀렸습니다.'}), 401

    # bcrypt 비밀번호 비교
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': '이메일 또는 비밀번호가 틀렸습니다.'}), 401

    user_obj = User(user['id'], user['username'], user['email'], user['password'])
    login_user(user_obj)
    return jsonify({'message': '로그인 성공!', 'user_id': user['id']})


# API: 로그아웃
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': '로그아웃 성공!'})

# API: 현재 로그인한 사용자 정보
@app.route('/api/me')
def me():
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        })
    else:
        return jsonify(None)

# API: 프로필 수정
@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'error': '모든 필드를 입력하세요.'}), 400

    conn = get_db()
    try:
        conn.execute('UPDATE user SET username = ?, email = ? WHERE id = ?', (username, email, current_user.id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': '이미 존재하는 사용자명 또는 이메일입니다.'}), 400

    conn.close()
    return jsonify({'message': '프로필이 수정되었습니다.'})

# 프로필 비밀번호 변경 추가
@app.route('/api/profile/password', methods=['POST'])
@login_required
def update_password():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'error': '모든 필드를 입력하세요.'}), 400

    conn = get_db()
    user = conn.execute('SELECT * FROM user WHERE id = ?', (current_user.id,)).fetchone()

    if not user:
        conn.close()
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 400

    # 현재 비밀번호 확인
    if not bcrypt.checkpw(current_password.encode('utf-8'), user['password']):
        conn.close()
        return jsonify({'error': '기존 비밀번호가 일치하지 않습니다.'}), 400

    # 새 비밀번호 암호화
    new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    conn.execute('UPDATE user SET password = ? WHERE id = ?', (new_hashed_password, current_user.id))
    conn.commit()
    conn.close()

    return jsonify({'message': '비밀번호가 변경되었습니다.'})


# API: 트윗 조회
@app.route('/api/tweets')
def get_tweets():
    conn = get_db()
    tweets = conn.execute('''
        SELECT tweet.*, user.username
        FROM tweet JOIN user ON tweet.user_id = user.id
        ORDER BY tweet.id DESC
    ''').fetchall()

    results = []
    if current_user.is_authenticated:
        for tweet in tweets:
            liked = conn.execute('SELECT 1 FROM like WHERE user_id = ? AND tweet_id = ?', (current_user.id, tweet['id'])).fetchone()
            results.append({
                'id': tweet['id'],
                'content': tweet['content'],
                'user_id': tweet['user_id'],
                'username': tweet['username'],
                'likes_count': tweet['likes_count'],
                'liked_by_current_user': bool(liked)
            })
    else:
        for tweet in tweets:
            results.append({
                'id': tweet['id'],
                'content': tweet['content'],
                'user_id': tweet['user_id'],
                'username': tweet['username'],
                'likes_count': tweet['likes_count'],
                'liked_by_current_user': False
            })
    conn.close()
    return jsonify(results)

# API: 트윗 작성
@app.route('/api/tweet', methods=['POST'])
@login_required
def create_tweet():
    content = request.json.get('content')
    conn = get_db()
    conn.execute('INSERT INTO tweet (content, user_id) VALUES (?, ?)', (content, current_user.id))
    conn.commit()
    conn.close()
    return jsonify({'message': '트윗이 작성되었습니다.'})

# API: 트윗 삭제
@app.route('/api/tweet/<int:tweet_id>', methods=['DELETE'])
@login_required
def delete_tweet(tweet_id):
    conn = get_db()
    tweet = conn.execute('SELECT * FROM tweet WHERE id = ?', (tweet_id,)).fetchone()
    if not tweet or tweet['user_id'] != current_user.id:
        conn.close()
        return jsonify({'error': '삭제 권한이 없습니다.'}), 403
    conn.execute('DELETE FROM like WHERE tweet_id = ?', (tweet_id,))
    conn.execute('DELETE FROM tweet WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '트윗이 삭제되었습니다.'})

# API: 좋아요
@app.route('/api/like/<int:tweet_id>', methods=['POST'])
@login_required
def like_tweet(tweet_id):
    conn = get_db()
    conn.execute('INSERT INTO like (user_id, tweet_id) VALUES (?, ?)', (current_user.id, tweet_id))
    conn.execute('UPDATE tweet SET likes_count = likes_count + 1 WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '좋아요!'})

# API: 좋아요 취소
@app.route('/api/unlike/<int:tweet_id>', methods=['POST'])
@login_required
def unlike_tweet(tweet_id):
    conn = get_db()
    conn.execute('DELETE FROM like WHERE user_id = ? AND tweet_id = ?', (current_user.id, tweet_id))
    conn.execute('UPDATE tweet SET likes_count = likes_count - 1 WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '좋아요 취소'})

# 정적 파일 제공
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
