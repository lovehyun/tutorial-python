from flask import Blueprint, render_template, session, jsonify
from database.db_sqlite import query_db, execute_db

hashtag_bp = Blueprint('hashtag', __name__)

@hashtag_bp.route('/hashtag/<int:music_id>/<int:hashtag_id>', methods=['DELETE'])
def delete_hashtag(music_id, hashtag_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    
    # 음악과 해시태그의 관계 삭제
    execute_db('DELETE FROM music_hashtag WHERE music_id=? AND hashtag_id=?', [music_id, hashtag_id])
    
    # 해당 해시태그가 더 이상 사용되지 않으면 해시태그 자체를 삭제
    remaining_usages = query_db('SELECT COUNT(*) as count FROM music_hashtag WHERE hashtag_id=?', [hashtag_id], one=True)
    if remaining_usages and remaining_usages['count'] == 0:
        execute_db('DELETE FROM hashtag WHERE hashtag_id=?', [hashtag_id])

    return '', 204

@hashtag_bp.route('/hashtags')
def hashtags():
    hashtag_data = query_db('''
        SELECT h.tag, COUNT(mh.music_id) as count
        FROM hashtag h
        JOIN music_hashtag mh ON h.hashtag_id = mh.hashtag_id
        GROUP BY h.tag
        ORDER BY count DESC
    ''')

    return render_template('hashtags.html', hashtag_data=hashtag_data)
