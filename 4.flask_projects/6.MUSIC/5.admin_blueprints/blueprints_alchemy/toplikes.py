from flask import Blueprint, render_template
from database.db_sqlalchemy import db, Music, User, Like
from sqlalchemy import func

toplikes_bp = Blueprint('toplikes', __name__)

@toplikes_bp.route('/toplikes', methods=['GET'])
def toplikes():
    # 데이터베이스에서 상위 좋아요 데이터를 가져오는 로직
    top_likes = db.session.execute(
        db.select(
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

    # 템플릿에 데이터 전달
    top_likes_data = [
        {
            'music_id': row.Music.music_id,
            'title': row.Music.title,
            'artist': row.Music.artist,
            'album_image': row.Music.album_image,
            'like_count': row.like_count,
            'liked_users': row.liked_users,
            'rank': row.rank,
        }
        for row in top_likes
    ]
    return render_template('toplikes.html', toplikes=top_likes_data)
