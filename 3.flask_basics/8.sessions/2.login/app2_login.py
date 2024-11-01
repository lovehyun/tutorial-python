from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션 암호화를 위한 키 설정

# 사용자 목록
users = [
    {'name': 'Alice', 'id': 'alice', 'pw': 'alice'},
    {'name': 'Bob', 'id': 'bob', 'pw': 'bob1234'},
    {'name': 'Charlie', 'id': 'charlie', 'pw': 'hello'},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # POST 방식의 FORM-Data 에서 id와 password 가져오기
        id = request.form['id']
        pw = request.form['password']

        # 사용자 목록과 매칭 확인
        user = next((user for user in users if user['id'] == id and user['pw'] == pw), None)

        if user:
            session['user'] = user  # 로그인한 사용자 정보를 세션에 저장
            error = None
            return redirect(url_for('profile'))
        else:
            error = "Invalid ID or password"

        return render_template('index2.html', error=error)

    return render_template('index2.html')

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile2.html', user=user)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # 세션에서 사용자 정보 삭제
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
