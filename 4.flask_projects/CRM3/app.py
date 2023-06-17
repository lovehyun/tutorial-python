import os

from apps.app_item import blueprint as item_blueprint
from apps.app_order import blueprint as order_blueprint
from apps.app_store import blueprint as store_blueprint
from apps.app_user import blueprint as user_blueprint

from database.model import db

from flask import Flask, redirect


app = Flask(__name__)

# DB 셋업
app.instance_path = os.getcwd()
db_url = 'sqlite:///' + os.path.join(app.instance_path, 'database', 'user-sample.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# URL Prefix 설정
url_prefix = os.environ.get('URL_PREFIX', '/')

# 포트 설정
port = int(os.environ.get('PORT', 5000))

# DB 초기화
db.init_app(app)

# 각종 애플리케이션 라우팅 설정 로딩
app.register_blueprint(item_blueprint, url_prefix=url_prefix)
app.register_blueprint(order_blueprint, url_prefix=url_prefix)
app.register_blueprint(store_blueprint, url_prefix=url_prefix)
app.register_blueprint(user_blueprint, url_prefix=url_prefix)


@app.route(url_prefix)
def landing():
    '''
    default landing page
    '''
    return redirect(url_prefix.rstrip('/') + '/users')

if __name__ == '__main__':
    print(f'Starting app with url_prefix={url_prefix}')
    with app.app_context():
        db.create_all()

    app.debug = True
    app.run(host="0.0.0.0", port=port)
