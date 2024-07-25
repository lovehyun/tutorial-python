from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

# SQLite 외래 키 제약 조건 활성화
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User(user_id={self.user_id}, username="{self.username}", email="{self.email}", created_at={self.created_at})>'

class Music(db.Model):
    music_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    album_image = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Music(music_id={self.music_id}, title="{self.title}", artist="{self.artist}", created_at={self.created_at})>'

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id'), primary_key=True)
    liked_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'<Like(user_id={self.user_id}, music_id={self.music_id}, liked_at={self.liked_at})>'
  
class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f'<Comment(comment_id={self.comment_id}, music_id={self.music_id}, user_id={self.user_id}, content="{self.content}", created_at={self.created_at})>'

class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id', ondelete='CASCADE'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.comment_id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Notification(notification_id={self.notification_id}, user_id={self.user_id}, music_id={self.music_id}, message="{self.message}", is_read={self.is_read}, created_at={self.created_at})>'

class Hashtag(db.Model):
    hashtag_id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Hashtag(hashtag_id={self.hashtag_id}, tag="{self.tag}")>'

class MusicHashtag(db.Model):
    __tablename__ = 'music_hashtag'
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtag.hashtag_id'), primary_key=True)

    def __repr__(self):
        return f'<MusicHashtag(music_id={self.music_id}, hashtag_id={self.hashtag_id})>'
