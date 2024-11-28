from flask import Blueprint, render_template, request, session
from database.db_sqlalchemy import db, Music, Like, Hashtag, MusicHashtag

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search', '')
    user_id = session.get('user_id')
    
    musics = []
    if search_query:
        if search_query.startswith('#'):
            hashtag_query = search_query[1:]
            musics = db.session.execute(
                db.select(Music, Like, db.func.group_concat(Hashtag.tag, ',').label('hashtags'))
                .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == user_id))
                .outerjoin(MusicHashtag, Music.music_id == MusicHashtag.music_id)
                .outerjoin(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
                .where(Music.music_id.in_(
                    db.select(MusicHashtag.music_id)
                    .join(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
                    .filter(Hashtag.tag.like(f'%{hashtag_query}%'))
                ))
                .group_by(Music.music_id)
            ).all()
        else:
            musics = db.session.execute(
                db.select(Music, Like, db.func.group_concat(Hashtag.tag, ',').label('hashtags'))
                .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == user_id))
                .outerjoin(MusicHashtag, Music.music_id == MusicHashtag.music_id)
                .outerjoin(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
                .where(Music.title.like(f'%{search_query}%') | Music.artist.like(f'%{search_query}%'))
                .group_by(Music.music_id)
            ).all()
    else:
        musics = db.session.execute(
            db.select(Music, Like, db.func.group_concat(Hashtag.tag, ',').label('hashtags'))
            .outerjoin(Like, (Music.music_id == Like.music_id) & (Like.user_id == user_id))
            .outerjoin(MusicHashtag, Music.music_id == MusicHashtag.music_id)
            .outerjoin(Hashtag, MusicHashtag.hashtag_id == Hashtag.hashtag_id)
            .group_by(Music.music_id)
        ).all()

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
