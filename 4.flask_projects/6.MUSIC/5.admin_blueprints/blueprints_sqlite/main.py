from flask import Blueprint, render_template, request, session
from database.db_sqlite import query_db

main_bp = Blueprint('main', __name__)
@main_bp.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    user_id = session.get('user_id')
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
            ''', [user_id, hashtag_query])
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
            ''', [user_id, '%' + search_query + '%', '%' + search_query + '%'])
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
        ''', [user_id])

    return render_template('index.html', musics=musics, search_query=search_query)
