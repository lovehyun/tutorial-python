from flask import Blueprint, render_template, session, request, redirect, url_for
from database.db_sqlalchemy import db, User, Comment, Music

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    users = db.session.execute(db.select(User)).scalars().all()
    return render_template('manage_users.html', users=users)

@admin_bp.route('/admin/comments')
def manage_comments():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))

    comments = db.session.execute(
        db.select(Comment, User.username, Music.title.label('music_title'))
        .join(User, Comment.user_id == User.user_id)
        .join(Music, Comment.music_id == Music.music_id)
        .order_by(Comment.created_at.desc())
    ).all()

    # 딕셔너리 형태로 변환
    comments = [{'comment_id': c.Comment.comment_id, 'content': c.Comment.content, 'username': c.username, 'music_id': c.Comment.music_id, 'created_at': c.Comment.created_at, 'music_title': c.music_title} for c in comments]

    return render_template('manage_comments.html', comments=comments)

@admin_bp.route('/admin/comments/<int:comment_id>', methods=['POST'])
def admin_delete_comment(comment_id):
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))

    comment = db.session.get(Comment, comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('admin.manage_comments'))
