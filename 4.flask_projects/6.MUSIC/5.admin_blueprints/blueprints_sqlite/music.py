from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from database.db_sqlite import query_db, execute_db

music_bp = Blueprint('music', __name__)

@music_bp.route('/music/<int:music_id>', methods=['GET', 'POST'])
def music(music_id):
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({"error": "로그인이 필요합니다."}), 401

        if 'content' in request.form:
            content = request.form['content']
            execute_db('INSERT INTO comment (music_id, user_id, content) VALUES (?, ?, ?)', [music_id, session['user_id'], content])

            # 알림을 백엔드에서 처리
            # likes = query_db('SELECT user_id FROM likes WHERE music_id=?', [music_id])
            # for like in likes:
            #     if like['user_id'] != session['user_id']:
            #         message = f"New comment added by {session['username']}: {content}"
            #         execute_db('INSERT INTO notification (user_id, music_id, comment_id, message) VALUES (?, ?, (SELECT last_insert_rowid()), ?)', [like['user_id'], music_id, message])

        if 'hashtag' in request.form:
            hashtag = request.form['hashtag'].strip()
            if hashtag:
                hashtag_id = query_db('SELECT hashtag_id FROM hashtag WHERE tag=?', [hashtag], one=True)
                if not hashtag_id:
                    execute_db('INSERT INTO hashtag (tag) VALUES (?)', [hashtag])
                    hashtag_id = query_db('SELECT hashtag_id FROM hashtag WHERE tag=?', [hashtag], one=True)
                
                existing_music_hashtag = query_db('SELECT * FROM music_hashtag WHERE music_id=? AND hashtag_id=?', [music_id, hashtag_id['hashtag_id']], one=True)
                if not existing_music_hashtag:
                    execute_db('INSERT INTO music_hashtag (music_id, hashtag_id) VALUES (?, ?)', [music_id, hashtag_id['hashtag_id']])
    
        return redirect(url_for('music.music', music_id=music_id))  # 코멘트 작성 후 페이지 리다이렉트

    user_id = session.get('user_id')
    music = query_db('SELECT m.*, CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked FROM music m LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ? WHERE m.music_id=?', [user_id, music_id], one=True)
    comments = query_db('SELECT comment_id, content, created_at, user_id, (SELECT username FROM user WHERE user_id=comment.user_id) AS username FROM comment WHERE music_id=?', [music_id])
    hashtags = query_db('SELECT h.hashtag_id, h.tag FROM hashtag h JOIN music_hashtag mh ON h.hashtag_id = mh.hashtag_id WHERE mh.music_id=?', [music_id])

    return render_template('music.html', music=music, comments=comments, hashtags=hashtags)
