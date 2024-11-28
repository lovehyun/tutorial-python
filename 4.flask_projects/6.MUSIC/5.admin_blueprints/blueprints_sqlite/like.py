from flask import Blueprint, request, session, jsonify, url_for, redirect
from database.db_sqlite import query_db, execute_db

like_bp = Blueprint('like', __name__)

@like_bp.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    # 요청 처리 후 돌아갈 페이지 확인
    redirect_url = request.form.get('redirect_url') or url_for('main.index')

    existing_like = query_db('SELECT * FROM likes WHERE user_id=? AND music_id=?', [session['user_id'], music_id], one=True)
    if existing_like:
        execute_db('DELETE FROM likes WHERE user_id=? AND music_id=?', [session['user_id'], music_id])
    else:
        execute_db('INSERT INTO likes (user_id, music_id) VALUES (?, ?)', [session['user_id'], music_id])

    return redirect(redirect_url)  # 좋아요 후 이전 페이지로 리다이렉트
