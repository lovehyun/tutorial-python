from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row  # 이 설정을 통해 컬럼명을 키로 하는 딕셔너리 형태로 결과를 받을 수 있습니다
    return conn

# 목록을 JSON 으로 주는 API 엔드포인트
@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT rank, title, audience FROM movies')
    rows = cur.fetchall()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            'rank': row['rank'],
            'title': row['title'],
            'audience': row['audience']
        })
    return jsonify(movies)

# 프런트엔드 렌더링
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT rank, title, audience, link FROM movies')
    rows = cur.fetchall()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            'rank': row['rank'],
            'title': row['title'],
            'audience': row['audience'],
            'link': row['link']
        })
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
