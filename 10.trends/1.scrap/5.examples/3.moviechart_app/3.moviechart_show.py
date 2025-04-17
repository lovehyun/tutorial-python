from flask import Flask, render_template, send_from_directory
import sqlite3
import os

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

    return render_template("index.html", movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
