import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'users.db'

def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if 'db' not in g:
        g.db = connect_db()
    try:
        g.db.execute('SELECT 1')  # DB 연결이 유효한지 확인
    except sqlite3.OperationalError:  # 연결이 유효하지 않으면 재연결 시도
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # 입력된 비밀번호를 바이트로 인코딩
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user and bcrypt.checkpw(password, user['password']):
            flash('로그인 성공!', 'success')
            # return redirect(url_for('index'))
            return redirect(url_for('dashboard'))
        else:
            flash('로그인 실패. 사용자 이름 또는 비밀번호가 올바르지 않습니다.', 'danger')
    return render_template('login2_bootstrap.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # 입력된 비밀번호를 바이트로 인코딩
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())  # 비밀번호 해싱
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashed_password])
        db.commit()
        flash('회원가입 성공!', 'success')
        return redirect(url_for('login'))
    return render_template('register3_bootstrap.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard3.html')

if __name__ == '__main__':
    app.run(debug=True)
