# pip install pymysql  # 외부 mysql 사용 시
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database.db_sqlalchemy import db, User, Music, Like, Comment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/database/music.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(db.select(User).filter_by(username=username, password=password)).scalar()
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
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
        musics = db.session.execute(
            db.select(Music, Like)
            .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id']))
            .filter((Music.title.like(f'%{search_query}%')) | (Music.artist.like(f'%{search_query}%')))
        ).all()
    else:
        musics = db.session.execute(
            db.select(Music, Like)
            .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id']))
        ).all()

    # 쿼리 결과를 딕셔너리로 변환
    musics = [{'music_id': music.music_id, 'title': music.title, 'artist': music.artist, 'album_image': music.album_image, 'created_at': music.created_at, 'liked': bool(like)} for music, like in musics]

    return render_template('index.html', musics=musics, search_query=search_query)

@app.route('/music/<int:music_id>', methods=['GET', 'POST'])
def music(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    music = db.session.get(Music, music_id)
    comments = db.session.execute(
        db.select(Comment, User.username, User.user_id)
        .join(User, Comment.user_id == User.user_id)
        .filter(Comment.music_id == music_id)
    ).all()

    # 딕셔너리 형태로 변환
    comments = [{'comment_id': comment.Comment.comment_id, 'username': comment.username, 'user_id': comment.user_id, 'created_at': comment.Comment.created_at, 'content': comment.Comment.content} for comment in comments]

    if request.method == 'POST':
        content = request.form['content']
        new_comment = Comment(music_id=music_id, user_id=session['user_id'], content=content)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('music', music_id=music_id))  # 코멘트 작성 후 페이지 리다이렉트
    
    return render_template('music.html', music=music, comments=comments)

@app.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    existing_like = db.session.execute(
        db.select(Like).filter_by(user_id=session['user_id'], music_id=music_id)
    ).scalar()
    
    if existing_like:
        db.session.delete(existing_like)
    else:
        new_like = Like(user_id=session['user_id'], music_id=music_id)
        db.session.add(new_like)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/comment/<int:comment_id>', methods=['POST']) # form 을 사용함으로 GET/POST 만 지원
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    comment = db.session.get(Comment, comment_id)
    if comment and comment.user_id == session['user_id']:
        db.session.delete(comment)
        db.session.commit()
    
    return redirect(url_for('music', music_id=comment.music_id)) # 삭제후 페이지 리로딩

if __name__ == '__main__':
    app.run(debug=True)
