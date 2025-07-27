# routes/user_routes.py
# 사용자 인증 관련 라우트 (회원가입, 로그인, 로그아웃)

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from database import get_db_connection, create_user_upload_folder

user_bp = Blueprint('user', __name__)

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

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('quiz.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        remember = bool(request.form.get('remember'))
        
        if not username or not password:
            flash('사용자명과 비밀번호를 모두 입력해주세요.', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['email'])
            login_user(user_obj, remember=remember)
            flash(f'{username}님, 환영합니다!', 'success')
            
            # 로그인 후 원래 가려던 페이지로 리디렉션
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('quiz.dashboard'))
        else:
            flash('사용자명 또는 비밀번호가 올바르지 않습니다.', 'error')
    
    return render_template('login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('quiz.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        # 유효성 검사
        errors = []
        
        if not username or len(username) < 3:
            errors.append('사용자명은 3자 이상이어야 합니다.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('사용자명은 영문, 숫자, 언더스코어만 사용 가능합니다.')
        
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('올바른 이메일 주소를 입력해주세요.')
        
        if not password or len(password) < 6:
            errors.append('비밀번호는 6자 이상이어야 합니다.')
        
        if password != password_confirm:
            errors.append('비밀번호가 일치하지 않습니다.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # 중복 확인
        conn = get_db_connection()
        existing_user = conn.execute(
            'SELECT id FROM users WHERE username = ? OR email = ?', 
            (username, email)
        ).fetchone()
        
        if existing_user:
            flash('이미 사용 중인 사용자명 또는 이메일입니다.', 'error')
            conn.close()
            return render_template('register.html')
        
        # 사용자 생성
        password_hash = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        user_id = cursor.lastrowid
        
        # 기본 설정 생성
        cursor.execute('''
            INSERT INTO user_settings (user_id, mode, question_order, choice_order, question_limit)
            VALUES (?, 'study', 'original', 'original', 0),
                   (?, 'quiz', 'original', 'original', 0)
        ''', (user_id, user_id))
        
        conn.commit()
        conn.close()
        
        # 사용자 폴더 생성
        create_user_upload_folder(user_id)
        
        flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('register.html')

@user_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'{username}님, 안전하게 로그아웃되었습니다.', 'info')
    return redirect(url_for('user.login'))

@user_bp.route('/profile')
@login_required
def profile():
    # 사용자 통계 정보 가져오기
    conn = get_db_connection()
    
    # 업로드된 파일 수
    file_count = conn.execute(
        'SELECT COUNT(*) as count FROM quiz_files WHERE user_id = ?', 
        (current_user.id,)
    ).fetchone()['count']
    
    # 총 시험 횟수
    quiz_count = conn.execute(
        'SELECT COUNT(*) as count FROM quiz_results WHERE user_id = ?', 
        (current_user.id,)
    ).fetchone()['count']
    
    # 평균 점수
    avg_score = conn.execute(
        'SELECT AVG(score) as avg_score FROM quiz_results WHERE user_id = ?', 
        (current_user.id,)
    ).fetchone()['avg_score']
    
    # 최고 점수
    max_score = conn.execute(
        'SELECT MAX(score) as max_score FROM quiz_results WHERE user_id = ?', 
        (current_user.id,)
    ).fetchone()['max_score']
    
    conn.close()
    
    stats = {
        'file_count': file_count,
        'quiz_count': quiz_count,
        'avg_score': round(avg_score, 1) if avg_score else 0,
        'max_score': max_score if max_score else 0
    }
    
    return render_template('profile.html', stats=stats)

@user_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """AJAX로 비밀번호 변경"""
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')
    
    # 유효성 검사
    if not current_password:
        return jsonify({'success': False, 'message': '현재 비밀번호를 입력해주세요.'})
    
    if not new_password or len(new_password) < 6:
        return jsonify({'success': False, 'message': '새 비밀번호는 6자 이상이어야 합니다.'})
    
    # 현재 비밀번호 확인
    conn = get_db_connection()
    user = conn.execute(
        'SELECT password_hash FROM users WHERE id = ?', 
        (current_user.id,)
    ).fetchone()
    
    if not check_password_hash(user['password_hash'], current_password):
        conn.close()
        return jsonify({'success': False, 'message': '현재 비밀번호가 올바르지 않습니다.'})
    
    # 비밀번호 업데이트
    new_password_hash = generate_password_hash(new_password)
    conn.execute(
        'UPDATE users SET password_hash = ? WHERE id = ?',
        (new_password_hash, current_user.id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '비밀번호가 성공적으로 변경되었습니다.'})
    
@user_bp.route('/change_email', methods=['POST'])
@login_required
def change_email():
    """AJAX로 이메일 변경"""
    new_email = request.json.get('new_email', '').strip()
    
    # 유효성 검사
    if not new_email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', new_email):
        return jsonify({'success': False, 'message': '올바른 이메일 주소를 입력해주세요.'})
    
    # 이메일 중복 확인
    conn = get_db_connection()
    existing_user = conn.execute(
        'SELECT id FROM users WHERE email = ? AND id != ?', 
        (new_email, current_user.id)
    ).fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({'success': False, 'message': '이미 사용 중인 이메일 주소입니다.'})
    
    # 이메일 업데이트
    conn.execute(
        'UPDATE users SET email = ? WHERE id = ?',
        (new_email, current_user.id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': '이메일이 성공적으로 변경되었습니다.', 'new_email': new_email})
