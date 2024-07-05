import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'users.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_database():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('username', 'password'))
    except sqlite3.IntegrityError as e:
        print(f"Error creating user 'user1': {e}")
    db.commit()
    cursor.close()
    db.close()

def query_db(query, args=(), one=False):
    db = connect_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user is not None:
            flash('로그인 성공!', 'success')
            return redirect(url_for('index'))
        else:
            flash('로그인 실패. 사용자 이름 또는 비밀번호가 올바르지 않습니다.', 'danger')
    return render_template('login3_tailwind.html')

if __name__ == '__main__':
    init_database()  # 초기 데이터베이스 설정
    app.run(debug=True)
