# pip install flask-sqlalchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask 애플리케이션 생성
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db' # 경로가 상대 경로로 설정되어 있으면, 기본적으로 instance/ 폴더를 기준으로 파일을 저장
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./example.db' # 현재 디렉토리
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLAlchemy가 객체의 변경 사항을 추적할지 여부를 결정. Flask 에서는 비추천.

# Flask-SQLAlchemy 객체 생성
db = SQLAlchemy(app)

# 사용자 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)

# 데이터베이스 테이블 생성 (초기화)
with app.app_context():
    db.create_all()

    # 새로운 사용자 추가
    new_user = User(name='Alice', age=30)
    db.session.add(new_user)
    new_user = User(name='Bob', age=20)
    db.session.add(new_user)
    db.session.commit()

    # 모든 사용자 조회
    users = User.query.all()
    for user in users:
        print(user.name, user.age)
