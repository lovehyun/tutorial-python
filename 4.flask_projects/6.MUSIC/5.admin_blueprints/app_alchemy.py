from flask import Flask
from blueprints_alchemy import register_blueprints
from database.db_sqlalchemy import db
from config import Config

def create_app():
    app = Flask(__name__, static_url_path=Config.APPLICATION_ROOT + '/static')
    app.config.from_object(Config)

    # DB 초기화
    db.init_app(app)

    # Blueprint 등록
    register_blueprints(app)
    # print(app.url_map)

    # DB 생성
    with app.app_context():
        db.create_all()

    return app

# 여기에서 app 객체를 생성하여 gunicorn에서 사용할 수 있도록 함
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
