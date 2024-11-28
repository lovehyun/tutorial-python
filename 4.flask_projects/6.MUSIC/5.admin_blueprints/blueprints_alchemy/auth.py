from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db_sqlalchemy import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.execute(db.select(User).filter_by(username=username, password=password)).scalar()
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['is_admin'] = user.username == 'admin'
            return redirect(url_for('main.index'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = db.session.execute(
            db.select(User).filter((User.username == username) | (User.email == email))
        ).scalar()
        if existing_user:
            return 'User already exists!', 400
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')
