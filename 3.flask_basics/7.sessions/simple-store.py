# pip install Flask-Session Flask-SQLAlchemy

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

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

    return 'Session data has been set!'


@app.route('/get_session')
def get_session_data():
    username = session.get('username', 'Guest')

    return f'Username: {username}'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
