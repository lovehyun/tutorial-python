from flask import Blueprint, render_template, redirect, url_for
from database.db_sqlite import query_db

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/profile/<int:user_id>')
def profile(user_id):
    user = query_db('SELECT * FROM user WHERE user_id=?', [user_id], one=True)
    if not user:
        return redirect(url_for('main.index'))

    comments = query_db('''
        SELECT c.*, m.title AS music_title
        FROM comment c
        JOIN music m ON c.music_id = m.music_id
        WHERE c.user_id=?
        ORDER BY c.created_at DESC
    ''', [user_id])

    liked_music = query_db('''
        SELECT m.*
        FROM music m
        JOIN likes l ON m.music_id = l.music_id
        WHERE l.user_id=?
    ''', [user_id])

    return render_template('profile.html', user=user, comments=comments, liked_music=liked_music)

