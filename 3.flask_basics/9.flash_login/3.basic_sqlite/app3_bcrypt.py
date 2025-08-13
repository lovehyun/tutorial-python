# pip install bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
import sqlite3
import os
import bcrypt  # bcrypt 모듈 사용

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

DB_PATH = 'users.db'

# 주요 변경 포인트
# 변경 항목	                                    설명
# bcrypt.hashpw(plain_pw, bcrypt.gensalt())	    비밀번호 해시 생성
# bcrypt.checkpw(plain_pw, hashed_pw)	        비밀번호 검증
# SQLite의 password 컬럼 타입	                TEXT → BLOB 또는 password BLOB (해시값이 바이트이므로)

# 사용자 조회 및 로그인 검증
def get_user_for_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None


# 사용자 존재 여부 확인
def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

# 사용자 생성
def create_user(username, password, name):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                (username, hashed_pw, name))
    conn.commit()
    conn.close()

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                name TEXT NOT NULL
            )
        ''')
        # 테스트 사용자 추가
        hashed_pw = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
        cur.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)",
                    ('user', hashed_pw, 'MyName'))
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("id")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        name = request.form.get("name")

        if not username or not password or not confirm_password or not name:
            flash("모든 필드를 입력해주세요.", "warning")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("비밀번호가 일치하지 않습니다.", "danger")
            return redirect(url_for('register'))

        if get_user_by_username(username):
            flash("이미 존재하는 아이디입니다.", "danger")
            return redirect(url_for('register'))

        create_user(username, password, name)

        flash("회원가입이 완료되었습니다. 로그인해주세요.", "success")
        return redirect(url_for('home'))

    return render_template('register2.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_id = request.form.get('id')
        password = request.form.get('password')

        user = get_user_for_login(user_id, password)
        if user:
            session['user'] = {'id': user['id'], 'name': user['name']}
            flash("로그인에 성공했습니다.", "success")
            return redirect(url_for('user'))

        flash("ID/PW가 일치하지 않습니다.", "danger")
        return redirect(url_for('home'))
    else:
        if 'user' in session:
            flash("이미 로그인 된 사용자 입니다.", "warning")
            return redirect(url_for('user'))

        return redirect(url_for('home'))

@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user2.html', name=user['name'])

    flash("비정상 접근입니다. 로그인을 필요로 합니다.", "warning")
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
        flash("정상적으로 로그아웃 되었습니다.", "success")
    else:
        flash("이미 로그아웃 되었습니다.", "warning")

    return redirect(url_for('home'))

if __name__ == "__main__":
    # init_db()
    app.run(debug=True)
