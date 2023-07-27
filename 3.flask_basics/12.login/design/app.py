# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('로그인 되었습니다.', 'success')
            return redirect(url_for('main'))
        else:
            flash('아이디나 비밀번호가 잘못되었습니다.', 'danger')
            # return "아이디나 비밀번호가 잘못되었습니다."

    return redirect(url_for('main'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('main'))

@app.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        new_password = request.form['new_password']
        new_email = request.form['new_email']

        current_user.set_password(new_password)
        current_user.email = new_email
        db.session.commit()

        return redirect(url_for('main'))

    return render_template('profile_edit.html', current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('이미 사용 중인 아이디입니다.', 'danger')
            # return "이미 사용 중인 아이디입니다."
        else:
            new_user = User(username=username)
            if email:  # Check if email is provided
                new_user.email = email
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('계정이 생성되었습니다. 이제 로그인하세요!', 'info')
            return redirect(url_for('main'))

    return render_template('register.html')

@app.route('/profile_delete', methods=['POST'])
@login_required
def profile_delete():
    # 사용자 정보 삭제
    db.session.delete(current_user)
    db.session.commit()

    # 로그아웃 처리
    logout_user()

    return redirect(url_for('main'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
