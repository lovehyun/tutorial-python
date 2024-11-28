import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.getcwd()}/database/music.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLITE_DATABASE_PATH = 'database/music.db'

    # 환경변수에서 URL prefix 읽기 (기본값 '/')
    APPLICATION_ROOT = os.getenv('FLASK_APPLICATION_PREFIX', '/')
