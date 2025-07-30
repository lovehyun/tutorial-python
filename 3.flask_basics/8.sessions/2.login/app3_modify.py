from flask import Flask, render_template, request, session, redirect, url_for

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
    id = request.form['id']
    pw = request.form['password']

    # 사용자 목록과 매칭 확인
    user = next((u for u in users if u['id'] == id and u['pw'] == pw), None)

    if user:
        session['user'] = user  # 로그인한 사용자 정보를 세션에 저장
        return redirect(url_for('welcome'))
    else:
        error = "Invalid ID or password"
        return render_template('index2.html', error=error)

@app.route('/dashboard')
def welcome():
    user = session.get('user')
    if user:
        return render_template('dashboard2.html', name=user['name'])
    else:
        return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # 새 비밀번호를 폼에서 가져오기
        new_password = request.form['new_password'] # request.form.get('new_password')
        for u in users:
            if u['id'] == user['id']:
                u['pw'] = new_password  # 사용자 목록에서 비밀번호 업데이트
                break

        user['pw'] = new_password  # 세션에서 비밀번호 업데이트
        session['user'] = user  # 업데이트된 사용자 정보를 세션에 저장
        
        message = "Password successfully updated"
        
        return render_template('profile3.html', user=user, message=message)

    return render_template('profile3.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)  # 세션에서 사용자 정보 삭제
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
