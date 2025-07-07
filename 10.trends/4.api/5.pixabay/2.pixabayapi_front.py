from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': '검색어가 필요합니다.'}), 400

    pixabay_url = 'https://pixabay.com/api/'
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo',
        'per_page': 5
    }

    response = requests.get(pixabay_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({'error': 'Pixabay 요청 실패'}), 500

if __name__ == '__main__':
    app.run(debug=True)
