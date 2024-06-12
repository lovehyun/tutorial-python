# pip install Flask-Session Flask-SQLAlchemy

import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import json

# Flask 애플리케이션 생성
app = Flask(__name__)

# 비밀 키 설정 (환경 변수에서 가져오거나 기본값 사용)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# 데이터베이스 설정 (환경 변수에서 가져오거나 기본값 사용)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///sessions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Session 확장 사용 설정
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

# 세션 데이터 저장 라우트
@app.route('/')
def index():
    # 문자열 데이터 저장
    session['username'] = 'user'
    
    # 숫자 데이터 저장
    session['count'] = 42
    
    # 리스트 데이터 저장
    session['my_list'] = [1, 2, 3, 4, 5]
    
    # 세션 데이터 저장
    session_store(session.sid, dict(session))

    return 'Session data has been set!'

# 세션 데이터 가져오기 라우트
@app.route('/get_session')
def get_session_data_route():
    username = session.get('username', 'Guest')
    count = session.get('count', 0)
    my_list = session.get('my_list', [])

    # 세션 데이터 가져오기
    stored_session_data = get_session_data(session.sid)

    # 세션 데이터를 화면에 출력 가능한 문자열로 변환
    stored_session_str = json.dumps(stored_session_data, indent=4)

    # 세션 데이터를 화면에 출력
    return f'Username: {username}, Count: {count}, My List: {my_list}, Session Data: {stored_session_str}'

# 세션 데이터 저장 함수
def session_store(sid, data):
    session_data = SessionData.query.get(sid)
    if not session_data:
        session_data = SessionData(id=sid)
    session_data.data = json.dumps(data)
    db.session.add(session_data)
    db.session.commit()

# 세션 데이터 가져오기 함수
def get_session_data(sid):
    session_data = SessionData.query.get(sid)
    if session_data and session_data.data:
        return json.loads(session_data.data)
    return {}

# 세션 모델 정의
# 세션 모델 정의는 Flask-Session 확장을 사용하여 세션 데이터를 데이터베이스에 저장할 때 필요한 데이터베이스 테이블을 정의하는 것입니다. 
# Flask-Session은 다양한 세션 저장소를 지원하는데, 이 중 하나가 SQLAlchemy를 사용하여 세션 데이터를 관계형 데이터베이스에 저장하는 방법입니다.
class SessionData(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    data = db.Column(db.Text)

# 애플리케이션 실행
if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {e}")
