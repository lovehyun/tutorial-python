from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 사용자 인증 정보 (예: 데이터베이스에서 가져온 것처럼 사용)
users = {'username': 'password'}  # 예시 사용자 정보

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            flash('로그인 성공!', 'success')
            return redirect(url_for('index'))
        else:
            flash('로그인 실패. 사용자 이름 또는 비밀번호가 올바르지 않습니다.', 'danger')
    # return render_template('login.html')
    # return render_template('login2_bootstrap.html')
    return render_template('login3_tailwind.html')

if __name__ == '__main__':
    app.run(debug=True)
