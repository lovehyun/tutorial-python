from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

DB_PATH = 'users.db'

def get_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

@app.route('/')
def home():
    # return render_template('index.html')
    return render_template('index2.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user_id = request.form.get('id')
        password = request.form.get('password')

        user = get_user(user_id, password)
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
        # return render_template('user.html', name=user['name'])
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

@app.route("/register")
def register():
    flash("회원가입 기능은 아직 구현되지 않았습니다.", "info")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
