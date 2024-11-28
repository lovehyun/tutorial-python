from flask import Blueprint, request, session, jsonify, url_for, redirect
from database.db_sqlalchemy import db, Like

like_bp = Blueprint('like', __name__)

@like_bp.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    redirect_url = request.form.get('redirect_url') or url_for('main.index')

    existing_like = db.session.execute(
        db.select(Like).filter_by(user_id=session['user_id'], music_id=music_id)
    ).scalar()
    
    if existing_like:
        db.session.delete(existing_like)
    else:
        new_like = Like(user_id=session['user_id'], music_id=music_id)
        db.session.add(new_like)
    db.session.commit()
    
    return redirect(redirect_url)  # 좋아요 후 이전 페이지로 리다이렉트
