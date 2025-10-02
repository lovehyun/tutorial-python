# routes/__init__.py
# Blueprint 패키지 초기화 파일

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from .user_routes import user_bp
from .quiz_routes import quiz_bp
from .result_routes import result_bp

# 관리자 블루프린트 정의
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def admin_dashboard():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    return render_template('admin/dashboard.html')

# 사용자 목록
@admin_bp.route('/users')
def admin_users():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    from flask import request
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    conn = get_db_connection()
    total_count = conn.execute('SELECT COUNT(*) as c FROM users').fetchone()['c']
    users = conn.execute('''
        SELECT id, username, email, created_at, last_login_at, login_count, is_admin
        FROM users
        ORDER BY id ASC
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()
    conn.close()
    total_pages = (total_count + per_page - 1) // per_page
    return render_template('admin/users.html', users=users, page=page, total_pages=total_pages, total_count=total_count,
                           has_prev=page>1, has_next=offset+per_page<total_count)

@admin_bp.route('/users/add', methods=['POST'])
def admin_add_user():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    from werkzeug.security import generate_password_hash
    username = (url_for and None)  # placeholder to keep imports grouped
    # 실제 값은 폼에서 읽음
    from flask import request
    username = request.form.get('username','').strip()
    email = request.form.get('email','').strip()
    password = request.form.get('password','')
    if not username or not email or not password:
        flash('모든 필드를 입력해주세요.', 'error')
        return redirect(url_for('admin.admin_users'))
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, generate_password_hash(password)))
        conn.commit()
        flash('사용자가 추가되었습니다.', 'success')
    except Exception as e:
        flash(f'추가 중 오류: {e}', 'error')
    finally:
        conn.close()
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/users/<int:user_id>/update_email', methods=['POST'])
def admin_update_email(user_id):
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    from flask import request
    email = request.form.get('email','').strip()
    if not email:
        flash('이메일을 입력해주세요.', 'error')
        return redirect(url_for('admin.admin_users'))
    conn = get_db_connection()
    conn.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
    conn.commit()
    conn.close()
    flash('이메일이 변경되었습니다.', 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/users/<int:user_id>/update_password', methods=['POST'])
def admin_update_password(user_id):
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from flask import request
    from database import get_db_connection
    from werkzeug.security import generate_password_hash
    pw = request.form.get('password','')
    pw2 = request.form.get('password_confirm','')
    if not pw or pw != pw2 or len(pw) < 6:
        flash('비밀번호 조건이 올바르지 않습니다.', 'error')
        return redirect(url_for('admin.admin_users'))
    conn = get_db_connection()
    conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (generate_password_hash(pw), user_id))
    conn.commit()
    conn.close()
    flash('비밀번호가 변경되었습니다.', 'success')
    return redirect(url_for('admin.admin_users'))
    conn = get_db_connection()
    conn.execute('UPDATE users SET is_admin = CASE WHEN is_admin=1 THEN 0 ELSE 1 END WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('권한이 변경되었습니다.', 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def admin_delete_user(user_id):
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('사용자가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.admin_users'))

# 퀴즈 파일 목록
@admin_bp.route('/quizzes')
def admin_quizzes():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    from flask import request
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    conn = get_db_connection()
    total_count = conn.execute('SELECT COUNT(*) as c FROM quiz_files').fetchone()['c']
    rows = conn.execute('''
        SELECT qf.*, u.username as owner
        FROM quiz_files qf
        JOIN users u ON u.id = qf.user_id
        ORDER BY qf.created_at DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()
    conn.close()
    total_pages = (total_count + per_page - 1) // per_page
    return render_template('admin/quizzes.html', items=rows, page=page, total_pages=total_pages, total_count=total_count,
                           has_prev=page>1, has_next=offset+per_page<total_count)

# 시험 결과 목록 (학습 관리)
@admin_bp.route('/results')
def admin_results():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    from flask import request
    page = request.args.get('page', 1, type=int)
    per_page = 50
    offset = (page - 1) * per_page
    conn = get_db_connection()
    total_count = conn.execute('SELECT COUNT(*) as c FROM quiz_results').fetchone()['c']
    rows = conn.execute('''
        SELECT qr.*, u.username as username, qf.original_filename
        FROM quiz_results qr
        JOIN users u ON u.id = qr.user_id
        JOIN quiz_files qf ON qf.id = qr.quiz_file_id
        ORDER BY qr.created_at DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()
    conn.close()
    total_pages = (total_count + per_page - 1) // per_page
    return render_template('admin/results.html', items=rows, page=page, total_pages=total_pages, total_count=total_count,
                           has_prev=page>1, has_next=offset+per_page<total_count)

@admin_bp.route('/quizzes/<int:file_id>/toggle_public', methods=['POST'])
def admin_toggle_public(file_id):
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    conn = get_db_connection()
    conn.execute('UPDATE quiz_files SET is_public = CASE WHEN is_public=1 THEN 0 ELSE 1 END WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    flash('공개 상태가 변경되었습니다.', 'success')
    return redirect(url_for('admin.admin_quizzes'))

@admin_bp.route('/quizzes/<int:file_id>/delete', methods=['POST'])
def admin_delete_quiz(file_id):
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    conn = get_db_connection()
    conn.execute('DELETE FROM quiz_files WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    flash('퀴즈 파일이 삭제되었습니다.', 'success')
    return redirect(url_for('admin.admin_quizzes'))
@admin_bp.route('/results/<int:result_id>/delete', methods=['POST'])
def admin_delete_result(result_id):
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    conn = get_db_connection()
    conn.execute('DELETE FROM quiz_results WHERE id = ?', (result_id,))
    conn.commit()
    conn.close()
    flash('결과가 삭제되었습니다.', 'success')
    return redirect(url_for('admin.admin_results'))

# 관리자 통계
@admin_bp.route('/stats')
def admin_stats():
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        flash('관리자만 접근 가능합니다.', 'error')
        return redirect(url_for('quiz.dashboard'))
    from database import get_db_connection
    from datetime import datetime, timedelta
    conn = get_db_connection()
    counters = {}
    # 사용자 통계
    counters['users'] = conn.execute('SELECT COUNT(*) AS c FROM users').fetchone()['c']
    counters['total_logins'] = conn.execute('SELECT COALESCE(SUM(login_count),0) AS s FROM users').fetchone()['s']
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat(' ')
    counters['active_7d'] = conn.execute('SELECT COUNT(*) AS c FROM users WHERE last_login_at IS NOT NULL AND last_login_at >= ?', (seven_days_ago,)).fetchone()['c']
    # 퀴즈 통계
    counters['quizzes'] = conn.execute('SELECT COUNT(*) AS c FROM quiz_files').fetchone()['c']
    counters['public_quizzes'] = conn.execute('SELECT COUNT(*) AS c FROM quiz_files WHERE is_public = 1').fetchone()['c']
    counters['copied_quizzes'] = conn.execute('SELECT COUNT(*) AS c FROM quiz_files WHERE shared_source_file_id IS NOT NULL').fetchone()['c']
    # 결과/점수 통계
    counters['results'] = conn.execute('SELECT COUNT(*) AS c FROM quiz_results').fetchone()['c']
    counters['avg_score'] = conn.execute('SELECT ROUND(AVG(score),1) AS a FROM quiz_results').fetchone()['a'] or 0
    # 최근 7일 결과수 추이
    recent = conn.execute('''
        SELECT substr(created_at,1,10) as d, COUNT(*) as c
        FROM quiz_results
        WHERE created_at >= ?
        GROUP BY substr(created_at,1,10)
        ORDER BY d ASC
    ''', (seven_days_ago,)).fetchall()
    conn.close()
    trend = [{'date': r['d'], 'count': r['c']} for r in recent]
    return render_template('admin/stats.html', counters=counters, trend=trend)

__all__ = ['user_bp', 'quiz_bp', 'result_bp', 'admin_bp']
