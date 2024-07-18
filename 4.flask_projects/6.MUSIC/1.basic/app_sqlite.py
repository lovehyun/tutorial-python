from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database.db_sqlite import init_db, query_db, execute_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# 데이터베이스 초기화
init_db()

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search_query = ''
    if request.method == 'POST':
        search_query = request.form['search']
        musics = query_db('''
            SELECT m.*, 
                   CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked
            FROM music m
            LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ?
            WHERE m.title LIKE ? OR m.artist LIKE ?
        ''', [session['user_id'], '%' + search_query + '%', '%' + search_query + '%'])
    else:
        musics = query_db('''
            SELECT m.*, 
                   CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked
            FROM music m
            LEFT JOIN likes l ON m.music_id = l.music_id AND l.user_id = ?
        ''', [session['user_id']])
    
    return render_template('index.html', musics=musics, search_query=search_query)

@app.route('/music/<int:music_id>', methods=['GET', 'POST'])
def music(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    music = query_db('SELECT * FROM music WHERE music_id=?', [music_id], one=True)
    comments = query_db('SELECT comment_id, content, created_at, user_id, (SELECT username FROM user WHERE user_id=comment.user_id) AS username FROM comment WHERE music_id=?', [music_id])
    
    if request.method == 'POST':
        content = request.form['content']
        execute_db('INSERT INTO comment (music_id, user_id, content) VALUES (?, ?, ?)', [music_id, session['user_id'], content])
        return redirect(url_for('music', music_id=music_id))  # 코멘트 작성 후 페이지 리다이렉트

    return render_template('music.html', music=music, comments=comments)

@app.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    existing_like = query_db('SELECT * FROM likes WHERE user_id=? AND music_id=?', [session['user_id'], music_id], one=True)
    if existing_like:
        execute_db('DELETE FROM likes WHERE user_id=? AND music_id=?', [session['user_id'], music_id])
    else:
        execute_db('INSERT INTO likes (user_id, music_id) VALUES (?, ?)', [session['user_id'], music_id])
    return redirect(url_for('index'))

@app.route('/comment/<int:comment_id>', methods=['POST']) # form 을 사용함으로 GET/POST 만 지원
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    comment = query_db('SELECT * FROM comment WHERE comment_id=?', [comment_id], one=True)
    if comment and comment['user_id'] == session['user_id']:
        execute_db('DELETE FROM comment WHERE comment_id=?', [comment_id])
    return redirect(url_for('music', music_id=comment['music_id'])) # 삭제후 페이지 리로딩

if __name__ == '__main__':
    app.run(debug=True)
