from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessions.db'
db = SQLAlchemy(app)

# Flask-Session 확장 사용
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

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
class SessionData(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    data = db.Column(db.Text)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
