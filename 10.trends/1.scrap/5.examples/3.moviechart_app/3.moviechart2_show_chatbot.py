from flask import Flask, render_template, send_from_directory, request, jsonify
import sqlite3
import os
import random

app = Flask(__name__)

THUMBNAIL_FOLDER = os.path.join(os.getcwd(), 'thumbnails')

@app.route('/thumbnail/<filename>')
def serve_thumbnail(filename):
    return send_from_directory(THUMBNAIL_FOLDER, filename)

@app.route('/')
def index():
    conn = sqlite3.connect('moviechart.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies ORDER BY rank ASC")
    rows = cur.fetchall()
    conn.close()

    movies = []
    for row in rows:
        thumbnail_filename = os.path.basename(row['thumbnail_path']) if row['thumbnail_path'] else ''
        movies.append({
            'title': row['title'],
            'synopsis': row['synopsis'],
            'detail_link': row['detail_link'],
            'original_url': row['original_url'],
            'thumbnail_filename': thumbnail_filename,
            'thumbnail_path': row['thumbnail_path']
        })

    return render_template("index2_chatbot.html", movies=movies)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'answer': '무엇을 도와드릴까요? 질문을 입력해주세요.'})

    conn = sqlite3.connect('moviechart.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT title, synopsis FROM movies")
    all_movies = cur.fetchall()
    conn.close()

    # 추천 요청 처리
    if '추천' in question:
        random_movie = random.choice(all_movies)
        return jsonify({'answer': f'🎬 추천 영화: "{random_movie["title"]}"'})

    # 시놉시스 키워드 매칭
    matched_titles = []
    for row in all_movies:
        if question in row['synopsis']:
            matched_titles.append(row['title'])

    if matched_titles:
        return jsonify({'answer': '🔍 관련 영화: ' + ', '.join(matched_titles)})
    else:
        return jsonify({'answer': '일치하는 영화가 없습니다.'})

if __name__ == '__main__':
    app.run(debug=True)
