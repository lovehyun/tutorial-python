from flask import Blueprint, render_template, session, redirect, url_for
from database.db_sqlalchemy import db, User, Comment, Music, Like

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile/<int:user_id>')
def profile(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for('main.index'))

    comments = db.session.execute(
        db.select(Comment, Music.title.label('music_title'))
        .join(Music, Comment.music_id == Music.music_id)
        .filter(Comment.user_id == user_id)
        .order_by(Comment.created_at.desc())
    ).all()

    liked_music = db.session.execute(
        db.select(Music)
        .join(Like, Like.music_id == Music.music_id)
        .filter(Like.user_id == user_id)
    ).all()

    comments = [{'content': c.Comment.content, 'music_id': c.Comment.music_id, 'created_at': c.Comment.created_at, 'music_title': c.music_title} for c in comments]
    liked_music = [{'music_id': m.Music.music_id, 'title': m.Music.title, 'artist': m.Music.artist} for m in liked_music]

    return render_template('profile.html', user=user, comments=comments, liked_music=liked_music)
