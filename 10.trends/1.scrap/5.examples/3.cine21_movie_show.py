from flask import Flask, render_template_string
import sqlite3
import base64

app = Flask(__name__)
DB_PATH = 'movies.db'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>영화 박스오피스</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; border: 1px solid #ccc; text-align: center; }
        img { max-height: 100px; }
    </style>
</head>
<body>
    <h2>🎬 박스오피스 영화 목록</h2>
    <table>
        <thead>
            <tr>
                <th>순위</th>
                <th>제목</th>
                <th>관객 수</th>
                <th>이미지</th>
                <th>상세 링크</th>
            </tr>
        </thead>
        <tbody>
            {% for movie in movies %}
            <tr>
                <td>{{ movie.rank }}</td>
                <td>{{ movie.title }}</td>
                <td>{{ movie.audience }}</td>
                <td>
                    {% if movie.poster_blob %}
                        <img src="data:image/jpeg;base64,{{ movie.poster_base64 }}" alt="poster">
                    {% else %}
                        (없음)
                    {% endif %}
                </td>
                <td><a href="{{ movie.detail_link }}" target="_blank">링크</a></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies ORDER BY scraped_at DESC, rank ASC")
    rows = cur.fetchall()
    conn.close()

    # base64 이미지 처리
    movies = []
    for row in rows:
        poster_blob = row['poster_blob']
        poster_base64 = base64.b64encode(poster_blob).decode('utf-8') if poster_blob else None
        movies.append({
            'rank': row['rank'],
            'title': row['title'],
            'audience': row['audience'],
            'detail_link': row['detail_link'],
            'poster_base64': poster_base64,
            'poster_blob': poster_blob
        })

    return render_template_string(HTML_TEMPLATE, movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
