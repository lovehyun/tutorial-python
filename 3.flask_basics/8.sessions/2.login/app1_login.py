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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # POST 방식의 FORM-Data 에서 id와 password 가져오기
        id = request.form['id'] # request.form.get('id')
        pw = request.form['password'] # request.form.get('password')

        # 사용자 목록과 매칭 확인
        user = next((user for user in users if user['id'] == id and user['pw'] == pw), None)

        if user:
            session['user'] = user  # 로그인한 사용자 정보를 세션에 저장
            error = None
            return "Login Successful"
        else:
            error = "Invalid ID or password"

        return render_template('index.html', error=error)

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # 세션에서 사용자 정보 삭제
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
