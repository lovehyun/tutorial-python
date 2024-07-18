from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now)

class Music(db.Model):
    music_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    album_image = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now)

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, primary_key=True)
    liked_at = db.Column(db.TIMESTAMP, default=lambda: datetime.now)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now)
