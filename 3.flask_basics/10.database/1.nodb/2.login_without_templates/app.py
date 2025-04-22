from flask import Flask, request, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# DB 초기화 - 이거는 thread-safe 하지 않기 때문에, 라우트 함수에서 별도로 connect/close 하는것 권장
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
# 초기 데이터 (필요시 주석 제거)
# cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('user1', 'password1'))
# cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('user2', 'password2'))
# cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('user3', 'password3'))
# conn.commit()

# 정적 HTML 페이지
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    row = cursor.fetchone()

    if row:
        return '로그인 성공!'
    else:
        return '로그인 실패. 아이디 또는 비밀번호를 확인하세요.'

if __name__ == '__main__':
    app.run(debug=True)
