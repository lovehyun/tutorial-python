from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 데이터 암호화에 사용되는 키

# 세션 설정: 서버 메모리에 세션 저장
app.config['SESSION_TYPE'] = 'null'  # 서버 메모리에 저장
# app.config['SESSION_TYPE'] = 'filesystem'  # 서버 파일시스템에 저장
app.config['SESSION_PERMANENT'] = False  # 세션의 영구적 저장 여부 (옵션) - False는 브라우저 닫히면 삭제
app.config['SESSION_USE_SIGNER'] = True  # 세션 쿠키에 서명 사용
Session(app)  # Flask-Session 초기화

# 세션 설정 예제
@app.route('/set-session')
def set_session():
    session['username'] = 'test_user'  # 서버 측에 저장
    return "Session has been set!"

# 세션 가져오기 예제
@app.route('/get-session')
def get_session():
    username = session.get('username')
    if username:
        return f"Session value: {username}"
    else:
        return "No session value found!"

# 세션 삭제 예제
@app.route('/clear-session')
def clear_session():
    session.pop('username', None)
    return "Session has been cleared!"

if __name__ == '__main__':
    app.run(debug=True)