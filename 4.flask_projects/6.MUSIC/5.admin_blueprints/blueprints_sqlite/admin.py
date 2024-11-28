from flask import Blueprint, render_template, session, request, redirect, url_for
from database.db_sqlite import query_db, execute_db

admin_bp = Blueprint('admin', __name__)

# 관리자 기능
@admin_bp.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        execute_db('DELETE FROM user WHERE user_id=?', [user_id])
        # 아래는 trigger 로 자동으로 지워짐
        # execute_db('DELETE FROM comment WHERE user_id=?', [user_id])
        # execute_db('DELETE FROM likes WHERE user_id=?', [user_id])
        # execute_db('DELETE FROM notification WHERE user_id=?', [user_id])
    
    users = query_db('SELECT * FROM user')
    return render_template('manage_users.html', users=users)

@admin_bp.route('/admin/comments')
def manage_comments():
    if not session.get('is_admin'):
        return redirect(url_for('main.login'))

    comments = query_db('''
        SELECT c.*, u.username, m.title as music_title
        FROM comment c
        JOIN user u ON c.user_id = u.user_id
        JOIN music m ON c.music_id = m.music_id
        ORDER BY c.created_at DESC
    ''')

    return render_template('manage_comments.html', comments=comments)

@admin_bp.route('/admin/comments/<int:comment_id>', methods=['POST'])
def admin_delete_comment(comment_id):
    if not session.get('is_admin'):
        return redirect(url_for('lauth.ogin'))

    comment = query_db('SELECT * FROM comment WHERE comment_id=?', [comment_id], one=True)
    if comment:
        execute_db('DELETE FROM comment WHERE comment_id=?', [comment_id])
    
    return redirect(url_for('admin.manage_comments'))
