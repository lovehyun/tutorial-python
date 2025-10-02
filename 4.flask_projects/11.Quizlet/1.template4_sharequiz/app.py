# app.py
# Flask 애플리케이션 메인 파일

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from datetime import timedelta

# 로컬 모듈 import
from database import init_database, get_db_connection, DB_PATH, UPLOAD_PATH
from migration import run_migrations
from routes.user_routes import user_bp
from routes.quiz_routes import quiz_bp
from routes.result_routes import result_bp
from routes import admin_bp
from migration import run_migrations

app = Flask(__name__)

# 설정
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
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
        self.is_admin = False
    
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
        u = User(user['id'], user['username'], user['email'])
        u.is_admin = bool(user['is_admin']) if 'is_admin' in user.keys() else False
        return u
    return None

# Blueprint 등록
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(quiz_bp, url_prefix='/quiz')
app.register_blueprint(result_bp, url_prefix='/result')
app.register_blueprint(admin_bp)

# 앱 로드 시점에 DB 준비 (개발/운영 모두 보장)
try:
    if not os.path.exists(DB_PATH):
        print("데이터베이스가 없습니다. 초기화를 진행합니다...")
        init_database()
    else:
        print("기존 데이터베이스를 감지했습니다. 마이그레이션을 실행합니다...")
        run_migrations()
        print("마이그레이션이 완료되었습니다.")
except Exception as e:
    print(f"DB 초기화/마이그레이션 중 오류: {e}")

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
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error/500.html'), 500

if __name__ == '__main__':
    # 환경에 따른 실행 모드
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    print("퀴즈 앱 서버를 시작합니다...")
    if debug_mode:
        print("개발 모드로 실행 중...")
        print("브라우저에서 http://localhost:5000 으로 접속하세요.")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Production 모드에서는 Gunicorn을 사용하세요:")
        print("gunicorn --bind 0.0.0.0:5000 --workers 4 --access-logfile - app:app")
        # Production에서는 직접 실행하지 않음
