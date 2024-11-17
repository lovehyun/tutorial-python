from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/search-lyrics', methods=['GET'])
def search_lyrics():
    query = request.args.get('query')

    try:
        response = requests.get('https://m.search.naver.com/p/csearch/content/qapirender.nhn', params={
            'where': 'm',
            'key': 'LyricsSearchResult',
            'pkid': '519',
            'u1': 1,
            'u2': 3,
            'u3': '0',
            'u4': '1',
            'q': '가사검색 ' + query,
        })

        app.logger.debug(response.json())  # 응답 내용을 출력

        current_html = response.json().get('current', {}).get('html', '')
        next_html = response.json().get('next', {}).get('html', '')

        current_results = process_lyrics_info(current_html)
        next_results = process_lyrics_info(next_html)

        all_results = current_results + next_results

        return jsonify(all_results)
    except Exception as error:
        app.logger.error('Error fetching lyrics: %s', error)
        return jsonify({'error': 'Internal Server Error'}), 500

def process_lyrics_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for element in soup.select('li[role="tab"]'):
        title = element.select_one('.music_title a').get_text(strip=True)
        artist = element.select_one('.music_detail a').get_text(strip=True)
        link = element.select_one('.music_title a')['href']
        lyrics = element.select_one('.lyrics_bx .lyrics_text').get_text(strip=True)

        results.append({
            'title': title,
            'artist': artist,
            'link': link,
            'lyrics': lyrics
        })

    return results

if __name__ == '__main__':
    app.run(port=5000, debug=True)
