from flask import Flask, render_template, request, redirect, url_for
from flask import session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션 암호화를 위한 키 설정

# 사용자 목록
users = [
    {'name': 'Alice', 'id': 'alice', 'pw': 'alice'},
    {'name': 'Bob', 'id': 'bob', 'pw': 'bob1234'},
    {'name': 'Charlie', 'id': 'charlie', 'pw': 'hello'},
]

@app.route('/', methods=['GET'])
def home():
    if session.get('user'):
        return redirect(url_for('welcome'))
    
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    # POST 방식의 FORM-Data 에서 id와 password 가져오기
    id = request.form['id'] # request.form.get('id')
    pw = request.form['password'] # request.form.get('password')

    # 사용자 목록과 매칭 확인
    user = next((u for u in users if u['id'] == id and u['pw'] == pw), None)

    if user:
        session['user'] = user  # 로그인한 사용자 정보를 세션에 저장
        error = None
        return redirect(url_for('welcome'))
    else:
        error = "Invalid ID or password"

    return render_template('index.html', error=error)

@app.route('/dashboard')
def welcome():
    user = session.get('user')
    if user:
        return render_template('dashboard2.html', name=user['name'])
    else:
        return redirect(url_for('home'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile2.html', user=user)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # 세션에서 사용자 정보 삭제  (키가 없을경우 None 반환해서 에러 발생 안하도록...)
                               # sessin.pop('user') 라고만 하면 'user' 키가 존재하면 pop, 키가 없으면 KeyError
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
