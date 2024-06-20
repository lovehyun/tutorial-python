from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

DATABASE_NAME = 'example.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db 와 app 연결
db.init_app(app)


@app.route('/')
def index():
    users = User.query.all()
    for user in users:
        print(user)  # This will call the __repr__ method of the User class
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    # GET 방식이었다면...
    # name = request.args.get('name')
    # age = request.args.get('age')
    
    name = request.form.get('name')
    age = request.form.get('age')
    if not name or not age:
        flash('Please enter both name and age')
        return redirect(url_for('index'))

    new_user = User(name=name, age=int(age))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 데이터베이스 초기화
    db_path = os.path.join(app.instance_path, DATABASE_NAME)
    if not os.path.exists(db_path):
        with app.app_context():
            print('DB 초기화...')
            db.create_all()

    # 사용자가 없으면, 기본 사용자 추가
    with app.app_context():
        # if not db.session.query(User).first():  # 둘다 동일한 코드
        if not User.query.first():
            print('사용자 초기화...')
            user1 = User(name="user1", age=30)
            user2 = User(name="user2", age=22)
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

    app.run(debug=True)
