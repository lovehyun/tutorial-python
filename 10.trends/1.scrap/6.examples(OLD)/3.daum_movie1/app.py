from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_movie_ranking():
    conn = sqlite3.connect('movie_data.db')
    cur = conn.cursor()

    cur.execute('''SELECT id, title, rating, reservation_rate, poster_link_url, short_description FROM movies''')
    data = cur.fetchall()
    conn.close()

    movie_rankings = []
    for row in data:
        rank, title, rating, reservation_rate, poster_link_url, short_description = row
        movie_rankings.append({
            'rank': rank,
            'title': title,
            'rating': rating,
            'reservation_rate': reservation_rate,
            'url': poster_link_url,
            'description': short_description
        })

    return movie_rankings

@app.route('/')
def index():
    movie_rankings = get_movie_ranking()

    return render_template('index.html', movie_rankings=movie_rankings)

if __name__ == '__main__':
    app.run(debug=True)
