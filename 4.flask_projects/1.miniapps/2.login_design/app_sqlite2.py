import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'users.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# 1. 요청시마다 매번 접속/종료
# def query_db(query, args=(), one=False):
#     db = connect_db()
#     cur = db.execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     db.close()
#     return (rv[0] if rv else None) if one else rv

# 2. 연결된 커넥션 지속 사용
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# 3. 연결된 커넥션 지속 사용 & 끊어지면 재연결
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
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user is not None:
            flash('로그인 성공!', 'success')
            return redirect(url_for('index'))
        else:
            flash('로그인 실패. 사용자 이름 또는 비밀번호가 올바르지 않습니다.', 'danger')
    # return render_template('login.html')
    # return render_template('login2_bootstrap.html')
    return render_template('login3_tailwind.html')

if __name__ == '__main__':
    app.run(debug=True)
