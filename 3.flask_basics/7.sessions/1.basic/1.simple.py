# curl -X GET http://127.0.0.1:5000/set_session/1234 -c cookies.txt
# curl -X GET http://127.0.0.1:5000/get_session -b cookies.txt

from flask import Flask, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 실제 운영에서는 보안에 강력한 랜덤 값으로 설정해야 합니다.

@app.route('/')
def index():
    # 세션에 데이터 저장
    session['username'] = 'user'
    session['data'] = '1234'

    return 'Session data has been set!'

@app.route('/set_session/<value>')
def set_session(value):
    session['data'] = value

    return f'Session data has been set: {value}'
    # return jsonify({"message": "Session value set", "value": value})

@app.route('/get_session')
def get_session_data():
    # 세션에서 데이터 가져오기 - 없으면 기본값으로 Guest 반납
    username = session.get('username', 'Guest')
    data = session.get('data', 'Not Set')
    
    # return f'Username: {username}, Data: {data}'
    return jsonify({"message": "Session value get", "username": username, "data": data})

if __name__ == '__main__':
    app.run()
