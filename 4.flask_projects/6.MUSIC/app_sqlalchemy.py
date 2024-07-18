# pip install pymysql
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database.db_sqlalchemy import db, User, Music, Like, Comment, Notification
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/music.db'
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
        user = User.query.filter_by(username=username, password=password).first()
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
        musics = db.session.query(Music, Like).outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id'])).filter(
            (Music.title.like(f'%{search_query}%')) | (Music.artist.like(f'%{search_query}%'))
        ).all()
    else:
        musics = db.session.query(Music, Like).outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id'])).all()
    
    notification_count = Notification.query.filter_by(user_id=session['user_id'], is_read=False).count()
    return render_template('index.html', musics=musics, notification_count=notification_count, search_query=search_query)

@app.route('/music/<int:music_id>', methods=['GET', 'POST'])
def music(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    music = Music.query.get(music_id)
    comments = db.session.query(Comment, User).join(User, Comment.user_id == User.user_id).filter(Comment.music_id == music_id).all()
    if request.method == 'POST':
        content = request.form['content']
        new_comment = Comment(music_id=music_id, user_id=session['user_id'], content=content)
        db.session.add(new_comment)
        db.session.commit()
        likes = Like.query.filter_by(music_id=music_id).all()
        for like in likes:
            if like.user_id != session['user_id']:
                new_notification = Notification(user_id=like.user_id, music_id=music_id, message=f"New comment on {music.title}")
                db.session.add(new_notification)
                db.session.commit()
    notification_count = Notification.query.filter_by(user_id=session['user_id'], is_read=False).count()
    return render_template('music.html', music=music, comments=comments, notification_count=notification_count)

@app.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    existing_like = Like.query.filter_by(user_id=session['user_id'], music_id=music_id).first()
    if existing_like:
        db.session.delete(existing_like)
    else:
        new_like = Like(user_id=session['user_id'], music_id=music_id)
        db.session.add(new_like)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    comment = Comment.query.get(comment_id)
    if comment and comment.user_id == session['user_id']:
        db.session.delete(comment)
        db.session.commit()
    return '', 204

@app.route('/notifications', methods=['GET', 'PUT'])
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        notifications = db.session.query(Notification, Music).join(Music, Notification.music_id == Music.music_id).filter(Notification.user_id == session['user_id']).all()
        notification_count = Notification.query.filter_by(user_id=session['user_id'], is_read=False).count()
        return render_template('notifications.html', notifications=notifications, notification_count=notification_count)
    elif request.method == 'PUT':
        notification_id = request.form['notification_id']
        new_status = request.form['new_status']
        notification = Notification.query.filter_by(notification_id=notification_id, user_id=session['user_id']).first()
        if notification:
            notification.is_read = bool(int(new_status))
            db.session.commit()
        return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
