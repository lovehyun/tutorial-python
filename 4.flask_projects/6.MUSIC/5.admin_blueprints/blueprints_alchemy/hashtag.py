from flask import Blueprint, render_template, session, jsonify
from database.db_sqlalchemy import db, Hashtag, MusicHashtag

hashtag_bp = Blueprint('hashtag', __name__)

@hashtag_bp.route('/hashtag/<int:music_id>/<int:hashtag_id>', methods=['DELETE'])
def delete_hashtag(music_id, hashtag_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    
    # 음악과 해시태그의 관계 삭제
    music_hashtag = db.session.execute(
        db.select(MusicHashtag).filter_by(music_id=music_id, hashtag_id=hashtag_id)
    ).scalar()
    
    if music_hashtag:
        db.session.delete(music_hashtag)
        db.session.commit()
    
    # 해당 해시태그가 더 이상 사용되지 않으면 해시태그 자체를 삭제
    remaining_usages = db.session.execute(
        db.select(db.func.count(MusicHashtag.music_id)).filter_by(hashtag_id=hashtag_id)
    ).scalar()
    
    if remaining_usages == 0:
        hashtag = db.session.get(Hashtag, hashtag_id)
        db.session.delete(hashtag)
        db.session.commit()

    return '', 204

@hashtag_bp.route('/hashtags', methods=['GET'])
def hashtags():
    hashtag_data = db.session.execute(
        db.select(Hashtag.tag, db.func.count(MusicHashtag.music_id).label('count'))
        .join(MusicHashtag, Hashtag.hashtag_id == MusicHashtag.hashtag_id)
        .group_by(Hashtag.tag)
        .order_by(db.func.count(MusicHashtag.music_id).desc())
    ).all()

    return render_template('hashtags.html', hashtag_data=hashtag_data)
