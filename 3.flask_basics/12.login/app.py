from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'secret_key'  # 보안을 위한 시크릿 키 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)

# Flask-Login 초기화
login_manager = LoginManager()
login_manager.init_app(app)

# 사용자 정보 모델
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# 사용자 로드 함수
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 사용자 생성 함수 (새로운 사용자 생성)
def create_user(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

# 로그인 뷰
@app.route('/login', methods=['POST'])
def login():
    # 실제로는 여기서 사용자 인증 처리를 해야합니다.
    user = User.query.filter_by(username='user1').first()
    login_user(user)
    return redirect(url_for('dashboard'))

# 로그아웃 뷰
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 로그인 필요한 보호된 뷰
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        # 데이터베이스 테이블 생성
        db.create_all()
    
        # 사용자 생성 (실행 시 한 번만 필요)
        # create_user('user1')
    
    app.run()
