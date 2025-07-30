from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abcd1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# 둘다 가능 함 (위에 방식을 더 추천)
# app.secret_key = 'abcd1234'
# app.permanent_session_lifetime = timedelta(minutes=5)

users = [
    {'name': 'MyName', 'id': 'user', 'pw': 'password'},
]

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = request.form.get('id')
        password = request.form.get('password')
        
        user = next((u for u in users if u["id"] == user and u["pw"] == password), None)
        if user:
            session['user'] = user
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
    app.run(debug=True)
