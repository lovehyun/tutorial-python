from flask import Blueprint, session, jsonify, url_for, redirect
from database.db_sqlalchemy import db, Comment

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comment/<int:comment_id>', methods=['POST']) # form 을 사용함으로 GET/POST 만 지원
def delete_comment(comment_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    
    comment = db.session.get(Comment, comment_id)
    if comment and comment.user_id == session['user_id']:
        db.session.delete(comment)
        db.session.commit()
    
    return redirect(url_for('music.music', music_id=comment.music_id)) # 삭제후 페이지 리로딩
