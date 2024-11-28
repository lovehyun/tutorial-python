from flask import Blueprint, g, session, redirect, url_for, jsonify, render_template, request
from database.db_sqlite import query_db, execute_db, get_notification_count

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notifications', methods=['GET', 'PUT'])
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
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
    