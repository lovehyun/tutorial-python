from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from database.db_sqlite import init_db, query_db, execute_db, get_notification_count

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# 데이터베이스 초기화
init_db()

# 모든 페이지에서 공통으로 필요로 하는 정보 추가
@app.before_request
def before_request():
    if 'user_id' in session:
        g.notification_count = get_notification_count(session['user_id'])
    else:
        g.notification_count = 0

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM user WHERE username=? AND password=?', [username, password], one=True)
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = request.args.get('search', '')
    musics = []

    if search_query:
        if search_query.startswith('#'):  # 해시태그 검색
            hashtag_query = search_query[1:]
            musics = query_db('''
                SELECT m.*, 
                       CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked,
                       GROUP_CONCAT(h.tag, ',') AS hashtags
                FROM music m
                LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ?
                LEFT JOIN music_hashtag mh ON m.music_id = mh.music_id
                LEFT JOIN hashtag h ON mh.hashtag_id = h.hashtag_id
                WHERE m.music_id IN (
                    SELECT m.music_id
                    FROM music m
                    JOIN music_hashtag mh ON m.music_id = mh.music_id
                    JOIN hashtag h ON mh.hashtag_id = h.hashtag_id
                    WHERE h.tag LIKE ?
                )
                GROUP BY m.music_id
            ''', [session['user_id'], hashtag_query])
        else:  # 일반 곡, 가수 검색
            musics = query_db('''
                SELECT m.*, 
                       CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked,
                       GROUP_CONCAT(h.tag, ',') AS hashtags
                FROM music m
                LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ?
                LEFT JOIN music_hashtag mh ON m.music_id = mh.music_id
                LEFT JOIN hashtag h ON mh.hashtag_id = h.hashtag_id
                WHERE m.title LIKE ? OR m.artist LIKE ?
                GROUP BY m.music_id
            ''', [session['user_id'], '%' + search_query + '%', '%' + search_query + '%'])
    else:  # 기본 전체쿼리
        musics = query_db('''
            SELECT m.*, 
                   CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked,
                   GROUP_CONCAT(h.tag, ',') AS hashtags
            FROM music m
            LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ?
            LEFT JOIN music_hashtag mh ON m.music_id = mh.music_id
            LEFT JOIN hashtag h ON mh.hashtag_id = h.hashtag_id
            GROUP BY m.music_id
        ''', [session['user_id']])

    return render_template('index.html', musics=musics, search_query=search_query)

@app.route('/music/<int:music_id>', methods=['GET', 'POST'])
def music(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    music = query_db('SELECT m.*, CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked FROM music m LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ? WHERE m.music_id=?', [session['user_id'], music_id], one=True)
    comments = query_db('SELECT comment_id, content, created_at, user_id, (SELECT username FROM user WHERE user_id=comment.user_id) AS username FROM comment WHERE music_id=?', [music_id])
    hashtags = query_db('SELECT h.hashtag_id, h.tag FROM hashtag h JOIN music_hashtag mh ON h.hashtag_id = mh.hashtag_id WHERE mh.music_id=?', [music_id])

    if request.method == 'POST':
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
                
                # Check if the hashtag is already associated with the music
                existing_music_hashtag = query_db('SELECT * FROM music_hashtag WHERE music_id=? AND hashtag_id=?', [music_id, hashtag_id['hashtag_id']], one=True)
                if not existing_music_hashtag:
                    execute_db('INSERT INTO music_hashtag (music_id, hashtag_id) VALUES (?, ?)', [music_id, hashtag_id['hashtag_id']])
    
        return redirect(url_for('music', music_id=music_id))  # 코멘트 작성 후 페이지 리다이렉트

    return render_template('music.html', music=music, comments=comments, hashtags=hashtags)

@app.route('/hashtag/<int:music_id>/<int:hashtag_id>', methods=['DELETE'])
def delete_hashtag(music_id, hashtag_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 음악과 해시태그의 관계 삭제
    execute_db('DELETE FROM music_hashtag WHERE music_id=? AND hashtag_id=?', [music_id, hashtag_id])
    
    # 해당 해시태그가 더 이상 사용되지 않으면 해시태그 자체를 삭제
    remaining_usages = query_db('SELECT COUNT(*) as count FROM music_hashtag WHERE hashtag_id=?', [hashtag_id], one=True)
    if remaining_usages and remaining_usages['count'] == 0:
        execute_db('DELETE FROM hashtag WHERE hashtag_id=?', [hashtag_id])

    return '', 204

@app.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 요청 처리 후 돌아갈 페이지 확인
    redirect_url = request.form.get('redirect_url') or url_for('index')

    existing_like = query_db('SELECT * FROM likes WHERE user_id=? AND music_id=?', [session['user_id'], music_id], one=True)
    if existing_like:
        execute_db('DELETE FROM likes WHERE user_id=? AND music_id=?', [session['user_id'], music_id])
    else:
        execute_db('INSERT INTO likes (user_id, music_id) VALUES (?, ?)', [session['user_id'], music_id])

    return redirect(redirect_url)  # 좋아요 후 이전 페이지로 리다이렉트

@app.route('/comment/<int:comment_id>', methods=['POST']) # form 을 사용함으로 GET/POST 만 지원
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    comment = query_db('SELECT * FROM comment WHERE comment_id=?', [comment_id], one=True)
    if comment and comment['user_id'] == session['user_id']:
        execute_db('DELETE FROM comment WHERE comment_id=?', [comment_id])
    return redirect(url_for('music', music_id=comment['music_id'])) # 삭제후 페이지 리로딩

@app.route('/notifications', methods=['GET', 'PUT'])
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        notifications = query_db('''
            SELECT n.*, m.title
            FROM notification n
            JOIN music m ON n.music_id = m.music_id
            WHERE n.user_id=?
            ORDER BY n.created_at DESC
        ''', [session['user_id']])
        return render_template('notifications.html', notifications=notifications)
    elif request.method == 'PUT':
        notification_id = request.form['notification_id']
        new_status = request.form['new_status']
        execute_db('UPDATE notification SET is_read=? WHERE notification_id=? AND user_id=?', [new_status, notification_id, session['user_id']])
        return jsonify(success=True)

@app.route('/hashtags')
def hashtags():
    hashtag_data = query_db('''
        SELECT h.tag, COUNT(mh.music_id) as count
        FROM hashtag h
        JOIN music_hashtag mh ON h.hashtag_id = mh.hashtag_id
        GROUP BY h.tag
        ORDER BY count DESC
    ''')

    return render_template('hashtags.html', hashtag_data=hashtag_data)

@app.route('/toplikes')
def toplikes():
    top_likes = query_db('''
        SELECT m.*, 
               COUNT(l.user_id) AS like_count,
               GROUP_CONCAT(u.username, ', ') AS liked_users,
               RANK() OVER (ORDER BY COUNT(l.user_id) DESC) AS rank
        FROM music m
        LEFT JOIN likes l ON m.music_id = l.music_id
        LEFT JOIN user u ON l.user_id = u.user_id
        GROUP BY m.music_id
        HAVING like_count > 0 -- 카운트가 0 인 것 제외
        ORDER BY like_count DESC
    ''')
    
    return render_template('toplikes.html', toplikes=top_likes)

if __name__ == '__main__':
    app.run(debug=True)
