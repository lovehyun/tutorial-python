from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # 객체를 출력할때의 포멧을 정의
    def __repr__(self):
        return f'<User {self.id}, {self.name}, {self.age}>'
