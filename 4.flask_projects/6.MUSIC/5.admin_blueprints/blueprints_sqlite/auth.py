from flask import Blueprint, render_template, session, request, redirect, url_for
from database.db_sqlite import query_db, execute_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM user WHERE username=? AND password=?', [username, password], one=True)
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['is_admin'] = user['username'] == 'admin'  # 관리자 여부를 세션에 저장
            return redirect(url_for('main.index'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)  # 관리자 여부 제거
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = query_db('SELECT * FROM user WHERE username=? OR email=?', [username, email], one=True)
        if existing_user:
            return 'User already exists!', 400
        execute_db('INSERT INTO user (username, password, email) VALUES (?, ?, ?)', [username, password, email])
        return redirect(url_for('auth.login'))
    return render_template('register.html')
