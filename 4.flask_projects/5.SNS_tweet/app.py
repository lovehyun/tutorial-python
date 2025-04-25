# pip install flask_login flask_wtf email-validator
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# 데이터베이스 모델 정의
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # 사용자가 특정 트윗을 좋아요하는 함수
    def like_tweet(self, tweet):
        if not self.has_liked(tweet):
            like = Like(user_id=self.id, tweet_id=tweet.id)
            db.session.add(like)
            tweet.likes_count += 1  # 트윗의 좋아요 수 증가
            db.session.commit()

    # 사용자가 특정 트윗의 좋아요를 취소하는 함수
    def unlike_tweet(self, tweet):
        like = Like.query.filter_by(user_id=self.id, tweet_id=tweet.id).first()
        if like:
            db.session.delete(like)
            tweet.likes_count -= 1  # 트윗의 좋아요 수 감소
            db.session.commit()

    # 사용자가 특정 트윗을 좋아요했는지 확인하는 함수
    def has_liked(self, tweet):
        return Like.query.filter_by(user_id=self.id, tweet_id=tweet.id).count() > 0

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    likes = db.relationship('Like', backref='tweet', lazy=True)
    likes_count = db.Column(db.Integer, default=0)  # 좋아요 수를 저장하는 필드 추가

class TweetForm(FlaskForm):
    content = TextAreaField('트윗', validators=[DataRequired(), Length(max=280)])
    submit = SubmitField('트윗하기')

class EditProfileForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    submit = SubmitField('저장')

# 로그인 관련 함수
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# 로그인 폼
class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('로그인')

# 회원가입 폼
class RegisterForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    submit = SubmitField('회원가입')

# 좋아요
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)


@app.route('/')
def index():
    tweets = Tweet.query.all()
    return render_template('index.html', tweets=tweets)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('로그인에 성공하였습니다!', 'success')
            return redirect(url_for('index'))
        else:
            flash('이메일 또는 비밀번호가 올바르지 않습니다.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('회원가입이 완료되었습니다!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required  # 로그인이 필요한 페이지
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('프로필이 수정되었습니다!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

@app.route('/tweet', methods=['GET'])
@login_required  # 로그인이 필요한 페이지
def tweet_form():
    form = TweetForm()
    return render_template('tweet.html', form=form)

@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
    form = TweetForm()
    if form.validate_on_submit():
        new_tweet = Tweet(content=form.content.data, user_id=current_user.id)
        db.session.add(new_tweet)
        db.session.commit()
        flash('트윗이 성공적으로 작성되었습니다!', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))  # 폼이 유효하지 않은 경우 인덱스 페이지로 리디렉션

@app.route('/like/<int:tweet_id>', methods=['POST'])
@login_required
def like_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    current_user.like_tweet(tweet)
    flash('트윗을 좋아합니다!', 'success')

    return redirect(url_for('index'))  # 원래 페이지로 리디렉션

@app.route('/unlike/<int:tweet_id>', methods=['POST'])
@login_required
def unlike_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    current_user.unlike_tweet(tweet)
    flash('좋아요를 취소했습니다.', 'info')
    return redirect(url_for('index'))  # 원래 페이지로 리디렉션

@app.route('/delete/<int:tweet_id>', methods=['POST'])
@login_required
def delete_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)

    if tweet.user_id != current_user.id:
        flash('삭제 권한이 없습니다.', 'danger')
        return redirect(url_for('index'))

    # 관련 좋아요 먼저 삭제 (foreign key 의존성 문제 방지)
    Like.query.filter_by(tweet_id=tweet.id).delete()
    db.session.delete(tweet)
    db.session.commit()
    flash('트윗이 삭제되었습니다.', 'success')
    return redirect(url_for('index'))

# db 초기화용 커맨드 등록
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print("데이터베이스가 초기화되었습니다.")

if __name__ == '__main__':
    # 데이터베이스 초기화
    with app.app_context():
        db.create_all()
    app.run(debug=True)
