# app.py
# Flask 애플리케이션 메인 파일

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from datetime import timedelta

# 로컬 모듈 import
from database import init_database, get_db_connection
from routes.user_routes import user_bp
from routes.quiz_routes import quiz_bp
from routes.result_routes import result_bp

app = Flask(__name__)

# 설정
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# ProxyFix 설정 (배포 시 필요)
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
login_manager.login_message = '로그인이 필요합니다.'
login_manager.login_message_category = 'warning'

# 사용자 로더
class User:
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    
    if user:
        return User(user['id'], user['username'], user['email'])
    return None

# Blueprint 등록
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(quiz_bp, url_prefix='/quiz')
app.register_blueprint(result_bp, url_prefix='/result')

# 메인 라우트
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('quiz.dashboard'))
    return redirect(url_for('user.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('quiz.dashboard'))

# 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

if __name__ == '__main__':
    # 데이터베이스 초기화 확인
    if not os.path.exists('quizlet.db'):
        print("데이터베이스가 없습니다. 초기화를 진행합니다...")
        init_database()
    
    # 환경에 따른 실행 모드
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    print("퀴즈 앱 서버를 시작합니다...")
    if debug_mode:
        print("개발 모드로 실행 중...")
        print("브라우저에서 http://localhost:5000 으로 접속하세요.")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Production 모드에서는 Gunicorn을 사용하세요:")
        print("gunicorn --bind 0.0.0.0:5000 --workers 4 app:app")
        # Production에서는 직접 실행하지 않음
