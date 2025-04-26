# pip install flask_login flask_wtf email-validator
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
app.secret_key = 'secret_key'

DATABASE = 'database.db'

login_manager = LoginManager()
login_manager.init_app(app)

# sqlite3 연결 헬퍼
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# User 모델을 수동으로 가져오기
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

# 로그인 관리
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# 폼
class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

class RegisterForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('회원가입')

class TweetForm(FlaskForm):
    content = TextAreaField('트윗', validators=[DataRequired(), Length(max=280)])
    submit = SubmitField('트윗하기')

class EditProfileForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('저장')

@app.route('/')
def index():
    conn = get_db()
    tweets = conn.execute('''
        SELECT tweet.*, user.username
        FROM tweet JOIN user ON tweet.user_id = user.id
        ORDER BY tweet.id DESC
    ''').fetchall()
    
    # 좋아요 정보를 추가로 가져오기
    tweets_with_like_info = []
    if current_user.is_authenticated:
        for tweet in tweets:
            like = conn.execute(
                'SELECT 1 FROM like WHERE user_id = ? AND tweet_id = ?',
                (current_user.id, tweet['id'])
            ).fetchone()
            tweets_with_like_info.append({
                **tweet,
                'liked_by_current_user': bool(like)
            })
    else:
        for tweet in tweets:
            tweets_with_like_info.append({
                **tweet,
                'liked_by_current_user': False
            })

    conn.close()

    # return render_template('index.html', tweets=tweets)
    return render_template('index.html', tweets=tweets_with_like_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user and user.password == form.password.data:
            login_user(user)
            flash('로그인 성공!', 'success')
            return redirect(url_for('index'))
        else:
            flash('이메일 또는 비밀번호가 틀렸습니다.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 완료!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                     (form.username.data, form.email.data, form.password.data))
        conn.commit()
        conn.close()
        flash('회원가입 완료!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute('UPDATE user SET username = ?, email = ? WHERE id = ?',
                     (form.username.data, form.email.data, current_user.id))
        conn.commit()
        conn.close()
        flash('프로필 수정 완료!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

@app.route('/tweet', methods=['GET', 'POST'])
@login_required
def tweet():
    form = TweetForm()
    if form.validate_on_submit():
        conn = get_db()
        conn.execute('INSERT INTO tweet (content, user_id) VALUES (?, ?)',
                     (form.content.data, current_user.id))
        conn.commit()
        conn.close()
        flash('트윗 작성 완료!', 'success')
        return redirect(url_for('index'))
    return render_template('tweet.html', form=form)

@app.route('/like/<int:tweet_id>', methods=['POST'])
@login_required
def like_tweet(tweet_id):
    conn = get_db()
    # 좋아요 기록 추가
    conn.execute('INSERT INTO like (user_id, tweet_id) VALUES (?, ?)', (current_user.id, tweet_id))
    # 트윗 좋아요 수 증가
    conn.execute('UPDATE tweet SET likes_count = likes_count + 1 WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()
    flash('좋아요 완료!', 'success')
    return redirect(url_for('index'))

@app.route('/unlike/<int:tweet_id>', methods=['POST'])
@login_required
def unlike_tweet(tweet_id):
    conn = get_db()
    conn.execute('DELETE FROM like WHERE user_id = ? AND tweet_id = ?', (current_user.id, tweet_id))
    conn.execute('UPDATE tweet SET likes_count = likes_count - 1 WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()
    flash('좋아요 취소!', 'info')
    return redirect(url_for('index'))

@app.route('/delete/<int:tweet_id>', methods=['POST'])
@login_required
def delete_tweet(tweet_id):
    conn = get_db()
    tweet = conn.execute('SELECT * FROM tweet WHERE id = ?', (tweet_id,)).fetchone()
    if not tweet or tweet['user_id'] != current_user.id:
        flash('삭제 권한이 없습니다.', 'danger')
        conn.close()
        return redirect(url_for('index'))

    conn.execute('DELETE FROM like WHERE tweet_id = ?', (tweet_id,))
    conn.execute('DELETE FROM tweet WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()
    flash('트윗 삭제 완료!', 'success')
    return redirect(url_for('index'))

# DB 초기화
@app.cli.command('init-db')
def init_db():
    conn = get_db()
    
    # DB 초기화 커맨드 파일로부터 실행
    # with open('init_database.sql', 'r', encoding='utf-8') as f:
    #     sql_script = f.read()
    # conn.executescript(sql_script)
    # conn.commit()
    # conn.close()
    # print("init_database.sql을 실행하여 데이터베이스가 초기화되었습니다!")

    # DB 초기화 커맨드 수행
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tweet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            likes_count INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS like (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tweet_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (tweet_id) REFERENCES tweet (id)
        )
    ''')
    conn.commit()
    conn.close()
    print("데이터베이스 초기화 완료!")

if __name__ == '__main__':
    with app.app_context():
        conn = get_db()
        conn.execute('PRAGMA foreign_keys = ON')  # SQLite에서 FK 강제
        conn.close()
    app.run(debug=True)
