from flask import Flask, request, jsonify, render_template, session
import sqlite3
import threading
import time
import uuid
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일에서 환경변수를 로드합니다.

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# 세션 관리를 위한 시간 저장 및 데이터베이스 저장
last_request_time = {}
db_connections = threading.local()
db_info = {}

@app.route('/')
def index():
    return render_template('index.html')

def get_db_connection():
    session_id = session.get('session_id')
    if session_id not in db_info:
        db_info[session_id] = {
            'db': sqlite3.connect(':memory:', check_same_thread=False),
            'created_at': time.time()
        }
        db = db_info[session_id]['db']
        cursor = db.cursor()
        cursor.execute("CREATE TABLE example (id INTEGER PRIMARY KEY, name TEXT)")
        db.commit()
    return db_info[session_id]['db']

@app.route('/query', methods=['POST'])
def query_db():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    session_id = session['session_id']

    db = get_db_connection()
    query = request.form['query']
    cursor = db.cursor()
    try:
        cursor.execute(query)
        db.commit()
        result = cursor.fetchall()
        response = {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': str(e)
        }
    last_request_time[session_id] = time.time()
    return jsonify(response)

@app.route('/db_info', methods=['GET'])
def get_db_info():
    session_id = session.get('session_id')
    if not session_id or session_id not in db_info:
        return jsonify({'status': 'error', 'message': 'No active session'}), 404

    db = db_info[session_id]['db']
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = {}
    table_counts = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema_info[table_name] = cursor.fetchall()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        table_counts[table_name] = cursor.fetchone()[0]

    response = {
        'status': 'success',
        'created_at': db_info[session_id]['created_at'],
        'last_request': last_request_time.get(session_id),
        'tables': tables,
        'schema': schema_info,
        'counts': table_counts
    }
    return jsonify(response)

@app.route('/entries/<table_name>', methods=['GET'])
def get_table_entries(table_name):
    session_id = session.get('session_id')
    if not session_id or session_id not in db_info:
        return jsonify({'status': 'error', 'message': 'No active session'}), 404

    db = db_info[session_id]['db']
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        entries = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        entries = [dict(zip(column_names, entry)) for entry in entries]
        return jsonify({'status': 'success', 'entries': entries})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def cleanup_sessions():
    session_timeout = int(os.getenv('SESSION_TIMEOUT', 3600)) # 기본값 1시간
    while True:
        time.sleep(60)  # 1분마다 세션 확인
        current_time = time.time()
        for sid, last_time in list(last_request_time.items()):
            if current_time - last_time > session_timeout:  # 환경변수에서 가져온 시간 경과
                if sid in db_info:
                    print(f"Closing session {sid}")
                    db_info[sid]['db'].close()
                    del db_info[sid]
                last_request_time.pop(sid, None)

cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
