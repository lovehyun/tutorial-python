from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import requests
from bs4 import BeautifulSoup
import re
import json
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/search-lyrics', methods=['GET'])
def search_lyrics():
    query = request.args.get('query')
    try:
        response = requests.get('https://m.search.naver.com/p/csearch/content/nqapirender.nhn', params={
            'callback': 'dummy',
            'where': 'nexearch',
            'key': 'LyricsSearchResult',
            'pkid': '519',
            'u1': 1,
            'u2': 5,
            'u3': 1,
            'u4': 1,
            'u5': query
        }, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        })

        raw_text = response.text.strip()

        # JSONP 파싱
        match = re.search(r'^dummy\((.*)\)\s*;?$', raw_text, re.DOTALL)
        if not match:
            app.logger.error("JSONP 파싱 실패")
            return jsonify({'error': 'Failed to parse response'}), 500

        json_str = match.group(1)
        data = json.loads(json_str)

        html = data.get("current", {}).get("html", "")
        results = process_lyrics_info(html)

        return jsonify(results)

    except Exception as error:
        app.logger.error('Error fetching lyrics: %s', error)
        return jsonify({'error': 'Internal Server Error'}), 500


def process_lyrics_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for element in soup.select('li._li'):
        title_tag = element.select_one('.music_title a')
        artist_tag = element.select_one('.sub_text')
        lyrics_tag = element.select_one('p.lyrics')

        if title_tag and artist_tag and lyrics_tag:
            results.append({
                'title': title_tag.get_text(strip=True),
                'artist': artist_tag.get_text(strip=True),
                'link': title_tag['href'],
                'lyrics': lyrics_tag.get_text(separator="\n", strip=True)
            })

    return results


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=True)
