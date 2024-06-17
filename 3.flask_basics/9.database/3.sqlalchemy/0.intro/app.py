from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 모델 import
from models import User

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    age = request.form.get('age')
    if not name or not age:
        flash('Please enter both name and age')
        return redirect(url_for('index'))

    new_user = User(name=name, age=int(age))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 데이터베이스 초기화
    if not os.path.exists('db.sqlite3'):
        db.create_all()
    app.run(debug=True)
