from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging

app = Flask(__name__)

def get_fetch_dates():
    conn = sqlite3.connect('movie_rankings.db')
    cur = conn.cursor()
    cur.execute('''SELECT DISTINCT fetch_date FROM weekly_rankings ORDER BY fetch_date DESC''')
    dates = cur.fetchall()
    conn.close()

    return [date[0] for date in dates]

def get_weekly_ranking(fetch_date):
    conn = sqlite3.connect('movie_rankings.db')
    cur = conn.cursor()

    app.logger.info("Fetching data for date: %s", fetch_date)

    cur.execute('''SELECT m.title, w.ranking, w.rating, w.reservation_rate, m.poster_img_url, m.poster_link_url
                   FROM movies m
                   JOIN weekly_rankings w ON m.id = w.movie_id
                   WHERE w.fetch_date = ? 
                   ORDER BY w.id''', (fetch_date,))
    data = cur.fetchall()
    conn.close()

    movie_rankings = []
    for row in data:
        title, rank, rating, reservation_rate, poster_img_url, poster_link_url = row
        movie_rankings.append({
            'title': title,
            'rank': rank,
            'rating': rating,
            'reservation_rate': reservation_rate,
            'img': poster_img_url,
            'url': poster_link_url,
        })

    return movie_rankings

@app.route('/')
def index():
    fetch_dates = get_fetch_dates()
    selected_fetch_date = request.args.get('fetch_date')

    if selected_fetch_date is not None:
        movie_rankings = get_weekly_ranking(selected_fetch_date)
    else:
        movie_rankings = []

    return render_template('index.html', fetch_dates=fetch_dates, selected_fetch_date=selected_fetch_date, movie_rankings=movie_rankings)

@app.route('/weekly_ranking')
def weekly_ranking():
    fetch_date = request.args.get('fetch_date')

    if fetch_date is not None:
        movie_rankings = get_weekly_ranking(fetch_date)
        return render_template('weekly_ranking2.html', fetch_date=fetch_date, movie_rankings=movie_rankings)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
