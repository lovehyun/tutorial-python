import os

from app.app_user import blueprint as user_blueprint
from app.app_order import blueprint as order_blueprint
from app.app_item import blueprint as item_blueprint
from app.app_store import blueprint as store_blueprint

from database.model import db

from flask import Flask, redirect


app = Flask(__name__)
app.instance_path = os.getcwd()
db_url = 'sqlite:///' + os.path.join(app.instance_path + '\database', 'user-sample.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(item_blueprint)
app.register_blueprint(store_blueprint)


@app.route('/')
def landing():
    '''
    default landing page
    '''
    return redirect('/users')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.debug = True
    app.run()
