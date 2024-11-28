from flask import Blueprint, render_template
from database.db_sqlite import query_db

toplikes_bp = Blueprint('toplikes', __name__)

@toplikes_bp.route('/toplikes')
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
