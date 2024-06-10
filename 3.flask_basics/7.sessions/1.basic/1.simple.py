from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 실제 운영에서는 보안에 강력한 랜덤 값으로 설정해야 합니다.

@app.route('/')
def index():
    # 세션에 데이터 저장
    session['username'] = 'user'
    session['data'] = '1234'
    return 'Session data has been set!'

@app.route('/get_session')
def get_session_data():
    # 세션에서 데이터 가져오기 - 없으면 기본값으로 Guest 반납
    username = session.get('username', 'Guest')
    return f'Username: {username}'

if __name__ == '__main__':
    app.run()
