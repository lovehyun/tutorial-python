from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from database.db_sqlalchemy import db, Music, User, Like, Comment, Hashtag, MusicHashtag

music_bp = Blueprint('music', __name__)

@music_bp.route('/music/<int:music_id>', methods=['GET', 'POST'])
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
    
        return redirect(url_for('music.music', music_id=music_id))  # 코멘트 및 해시태그 작성 후 페이지 리다이렉트
    
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
