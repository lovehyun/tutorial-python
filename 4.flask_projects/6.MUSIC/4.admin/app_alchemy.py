from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from database.db_sqlalchemy import db, User, Music, Like, Comment, Notification, Hashtag, MusicHashtag
from sqlalchemy import desc, select, func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/database/music.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# 모든 페이지에서 공통으로 필요로 하는 정보 추가
@app.before_request
def before_request():
    if 'user_id' in session:
        g.notification_count = db.session.execute(
            db.select(db.func.count(Notification.notification_id))
            .filter_by(user_id=session['user_id'], is_read=False)
        ).scalar()
    else:
        g.notification_count = 0

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(db.select(User).filter_by(username=username, password=password)).scalar()
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['is_admin'] = user.username == 'admin'  # 관리자 여부를 세션에 저장
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)  # 관리자 여부 제거
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalar()
        if existing_user:
            return 'User already exists!', 400
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for('index'))

    comments = db.session.execute(
        db.select(Comment, Music.title.label('music_title'))
        .join(Music, Comment.music_id == Music.music_id)
        .filter(Comment.user_id == user_id)
        .order_by(Comment.created_at.desc())
    ).all()

    liked_music = db.session.execute(
        db.select(Music)
        .join(Like, Like.music_id == Music.music_id)
        .filter(Like.user_id == user_id)
    ).all()

    # 딕셔너리 형태로 변환
    comments = [{'content': c.Comment.content, 'music_id': c.Comment.music_id, 'created_at': c.Comment.created_at, 'music_title': c.music_title} for c in comments]
    liked_music = [{'music_id': m.Music.music_id, 'title': m.Music.title, 'artist': m.Music.artist} for m in liked_music]

    return render_template('profile.html', user=user, comments=comments, liked_music=liked_music)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '')
    musics = []

    if search_query:
        if search_query.startswith('#'):  # 해시태그 검색
            hashtag_query = search_query[1:]
            musics = db.session.execute(
                db.select(Music, Like, db.func.group_concat(Hashtag.tag, ',').label('hashtags'))
                .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id']))
                .outerjoin(MusicHashtag, Music.music_id == MusicHashtag.music_id)
                .outerjoin(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
                .where(Music.music_id.in_(
                    db.select(MusicHashtag.music_id)
                    .join(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
                    .filter(Hashtag.tag.like(f'%{hashtag_query}%'))
                ))
                .group_by(Music.music_id)
            ).all()
        else:  # 일반 곡, 가수 검색
            musics = db.session.execute(
                db.select(Music, Like, db.func.group_concat(Hashtag.tag, ',').label('hashtags'))
                .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id']))
                .outerjoin(MusicHashtag, Music.music_id == MusicHashtag.music_id)
                .outerjoin(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
                .where(Music.title.like(f'%{search_query}%') | Music.artist.like(f'%{search_query}%'))
                .group_by(Music.music_id)
            ).all()
    else:  # 기본 전체쿼리
        musics = db.session.execute(
            db.select(Music, Like, db.func.group_concat(Hashtag.tag, ',').label('hashtags'))
            .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == session['user_id']))
            .outerjoin(MusicHashtag, Music.music_id == MusicHashtag.music_id)
            .outerjoin(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
            .group_by(Music.music_id)
        ).all()

    # 딕셔너리 형태로 변환
    musics = [{
        'music_id': music.Music.music_id, 
        'title': music.Music.title, 
        'artist': music.Music.artist, 
        'album_image': music.Music.album_image, 
        'created_at': music.Music.created_at, 
        'liked': 1 if music.Like else 0, 
        'hashtags': music.hashtags if music.hashtags else []
    } for music in musics]

    return render_template('index.html', musics=musics, search_query=search_query)

@app.route('/music/<int:music_id>', methods=['GET', 'POST'])
def music(music_id):
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({"error": "로그인이 필요합니다."}), 401

        if 'content' in request.form:
            content = request.form['content']
            new_comment = Comment(music_id=music_id, user_id=session['user_id'], content=content)
            db.session.add(new_comment)
            db.session.commit()
            
        if 'hashtag' in request.form:
            hashtag = request.form['hashtag'].strip()
            if hashtag:
                hashtag_obj = db.session.execute(
                    db.select(Hashtag).filter_by(tag=hashtag)
                ).scalar()
                if not hashtag_obj:
                    hashtag_obj = Hashtag(tag=hashtag)
                    db.session.add(hashtag_obj)
                    db.session.commit()

                # Check if the relationship already exists
                existing_music_hashtag = db.session.execute(
                    db.select(MusicHashtag).filter_by(music_id=music_id, hashtag_id=hashtag_obj.hashtag_id)
                ).scalar()
                if not existing_music_hashtag:
                    new_music_hashtag = MusicHashtag(music_id=music_id, hashtag_id=hashtag_obj.hashtag_id)
                    db.session.add(new_music_hashtag)
                    db.session.commit()
    
        return redirect(url_for('music', music_id=music_id))  # 코멘트 및 해시태그 작성 후 페이지 리다이렉트
    
    user_id = session.get('user_id')
    music = db.session.execute(
        db.select(Music, Like)
        .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == user_id))
        .filter(Music.music_id == music_id)
    ).one()
    
    # 코멘트 가져오기
    comments = db.session.execute(
        db.select(Comment, User.username, User.user_id)
        .join(User, Comment.user_id == User.user_id)
        .filter(Comment.music_id == music_id)
    ).all()
    
    # 해시태그 가져오기
    hashtags = db.session.execute(
        db.select(Hashtag.hashtag_id, Hashtag.tag)
        .join(MusicHashtag, Hashtag.hashtag_id == MusicHashtag.hashtag_id)
        .filter(MusicHashtag.music_id == music_id)
    ).all()
    
    # 딕셔너리 형태로 변환
    music_dict = {
        'music_id': music.Music.music_id, 
        'title': music.Music.title, 
        'artist': music.Music.artist, 
        'album_image': music.Music.album_image, 
        'created_at': music.Music.created_at, 
        'liked': 1 if music.Like else 0, 
    }
    comments = [{'comment_id': c.Comment.comment_id, 'username': c.username, 'user_id': c.user_id, 'created_at': c.Comment.created_at, 'content': c.Comment.content} for c in comments]
    hashtags = [{'hashtag_id': h.hashtag_id, 'tag': h.tag} for h in hashtags]

    return render_template('music.html', music=music_dict, comments=comments, hashtags=hashtags)

@app.route('/hashtag/<int:music_id>/<int:hashtag_id>', methods=['DELETE'])
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

@app.route('/like/<int:music_id>', methods=['POST'])
def like(music_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401

    redirect_url = request.form.get('redirect_url') or url_for('index')

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

@app.route('/comment/<int:comment_id>', methods=['POST']) # form 을 사용함으로 GET/POST 만 지원
def delete_comment(comment_id):
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401
    
    comment = db.session.get(Comment, comment_id)
    if comment and comment.user_id == session['user_id']:
        db.session.delete(comment)
        db.session.commit()
    
    return redirect(url_for('music', music_id=comment.music_id)) # 삭제후 페이지 리로딩

@app.route('/notifications', methods=['GET', 'PUT'])
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        notifications = db.session.execute(
            db.select(Notification, Music.title)
            .join(Music, Notification.music_id == Music.music_id)
            .filter(Notification.user_id == session['user_id'])
            .order_by(desc(Notification.created_at))
        ).all()
        
        # 딕셔너리 형태로 변환
        notifications = [{'notification_id': n.Notification.notification_id, 'message': n.Notification.message, 'title': n.title, 'created_at': n.Notification.created_at, 'is_read': n.Notification.is_read} for n in notifications]
        
        return render_template('notifications.html', notifications=notifications)
    elif request.method == 'PUT':
        notification_id = request.form['notification_id']
        new_status = request.form['new_status']
        
        notification = db.session.get(Notification, notification_id)
        if notification:
            notification.is_read = bool(int(new_status))
            db.session.commit()
        
        return jsonify(success=True)

@app.route('/hashtags')
def hashtags():
    hashtag_data = db.session.execute(
        db.select(Hashtag.tag, db.func.count(MusicHashtag.music_id).label('count'))
        .join(MusicHashtag, Hashtag.hashtag_id == MusicHashtag.hashtag_id)
        .group_by(Hashtag.tag)
        .order_by(db.func.count(MusicHashtag.music_id).desc())
    ).all()

    return render_template('hashtags.html', hashtag_data=hashtag_data)

@app.route('/toplikes')
def toplikes():
    top_likes = db.session.execute(
        select(
            Music,
            func.count(Like.user_id).label('like_count'),
            func.group_concat(User.username, ', ').label('liked_users'),
            func.rank().over(order_by=func.count(Like.user_id).desc()).label('rank')
        )
        .outerjoin(Like, Music.music_id == Like.music_id)
        .outerjoin(User, Like.user_id == User.user_id)
        .group_by(Music.music_id)
        .having(func.count(Like.user_id) > 0)
        .order_by(func.count(Like.user_id).desc())
    ).all()

    top_likes_data = []
    for row in top_likes:
        music_data = {
            'music_id': row.Music.music_id,
            'title': row.Music.title,
            'artist': row.Music.artist,
            'album_image': row.Music.album_image,
            'created_at': row.Music.created_at,
            'like_count': row.like_count,
            'liked_users': row.liked_users,
            'rank': row.rank,
        }
        top_likes_data.append(music_data)

    return render_template('toplikes.html', toplikes=top_likes_data)

# 관리자 기능
@app.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    users = db.session.execute(db.select(User)).scalars().all()
    return render_template('manage_users.html', users=users)

@app.route('/admin/comments')
def manage_comments():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    comments = db.session.execute(
        db.select(Comment, User.username, Music.title.label('music_title'))
        .join(User, Comment.user_id == User.user_id)
        .join(Music, Comment.music_id == Music.music_id)
        .order_by(Comment.created_at.desc())
    ).all()

    # 딕셔너리 형태로 변환
    comments = [{'comment_id': c.Comment.comment_id, 'content': c.Comment.content, 'username': c.username, 'music_id': c.Comment.music_id, 'created_at': c.Comment.created_at, 'music_title': c.music_title} for c in comments]

    return render_template('manage_comments.html', comments=comments)

@app.route('/admin/comments/<int:comment_id>', methods=['POST'])
def admin_delete_comment(comment_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    comment = db.session.get(Comment, comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('manage_comments'))

if __name__ == '__main__':
    app.run(debug=True)
