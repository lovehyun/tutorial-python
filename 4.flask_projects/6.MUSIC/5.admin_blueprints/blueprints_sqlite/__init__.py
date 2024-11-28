from .auth import auth_bp
from .main import main_bp
from .user import user_bp
from .admin import admin_bp
from .music import music_bp
from .comment import comment_bp
from .notification import notification_bp
from .hashtag import hashtag_bp
from .toplikes import toplikes_bp
from .like import like_bp

def register_blueprints(app):
    prefix = app.config['APPLICATION_ROOT']
    
    app.register_blueprint(auth_bp, url_prefix=prefix)
    app.register_blueprint(main_bp, url_prefix=prefix)
    app.register_blueprint(user_bp, url_prefix=prefix)
    app.register_blueprint(admin_bp, url_prefix=prefix)
    app.register_blueprint(music_bp, url_prefix=prefix)
    app.register_blueprint(comment_bp, url_prefix=prefix)
    app.register_blueprint(notification_bp, url_prefix=prefix)
    app.register_blueprint(hashtag_bp, url_prefix=prefix)
    app.register_blueprint(toplikes_bp, url_prefix=prefix)
    app.register_blueprint(like_bp, url_prefix=prefix)
