from flask import Blueprint, g, session, redirect, url_for, jsonify, render_template, request
from database.db_sqlalchemy import db, Notification, Music
from sqlalchemy import desc

notification_bp = Blueprint('notification', __name__)

@notification_bp.before_app_request
def load_notifications():
    if 'user_id' in session:
        g.notification_count = db.session.execute(
            db.select(db.func.count(Notification.notification_id))
            .filter_by(user_id=session['user_id'], is_read=False)
        ).scalar()
    else:
        g.notification_count = 0

@notification_bp.route('/notifications', methods=['GET', 'PUT'])
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
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