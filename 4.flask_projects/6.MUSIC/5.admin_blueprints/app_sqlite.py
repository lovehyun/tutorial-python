from flask import Flask, session, g
from blueprints_sqlite import register_blueprints
from database.db_sqlite import init_db, get_notification_count
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB 초기화
    init_db()

    @app.before_request
    def before_request():
        if 'user_id' in session:
            g.notification_count = get_notification_count(session['user_id'])
        else:
            g.notification_count = 0


    # Blueprint 등록
    register_blueprints(app)
    print(app.url_map)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
