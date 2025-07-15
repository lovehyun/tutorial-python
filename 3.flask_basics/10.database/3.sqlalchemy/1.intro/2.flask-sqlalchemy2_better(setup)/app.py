# pip install flask-sqlalchemy

from flask import Flask
from models import db

# 방법1.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # SQLAlchemy 의 내장 함수


# 방법2.
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) # SQLAlchemy 의 내장 함수

    # ---- Blueprint 등록 ----
    # from .routes import bp as main_bp
    # app.register_blueprint(main_bp)
    
    return app


# 실제 앱 실행
if __name__ == '__main__':
    # app = create_app()  # 좀 더 나은 초기화
    app.run(debug=True)
