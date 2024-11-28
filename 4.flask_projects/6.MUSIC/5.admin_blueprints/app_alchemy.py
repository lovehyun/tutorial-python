from flask import Flask
from blueprints_alchemy import register_blueprints
from database.db_sqlalchemy import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB 초기화
    db.init_app(app)

    # Blueprint 등록
    register_blueprints(app)
    print(app.url_map)

    # DB 생성
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
