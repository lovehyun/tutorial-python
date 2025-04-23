from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv, find_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv(find_dotenv('../.env'))

app = Flask(__name__)

# 카카오 API REST 키
KAKAO_RESTAPI_KEY = os.getenv("KAKAO_RESTAPI_KEY")

# 카카오 API 호출 함수
def call_kakao_api(api_url, params):
    headers = {
        "Authorization": f"KakaoAK {KAKAO_RESTAPI_KEY}"
    }
    response = requests.get(api_url, headers=headers, params=params)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    search_type = request.args.get('type')
    
    if search_type == 'web':
        api_url = 'https://dapi.kakao.com/v2/search/web'
    elif search_type == 'image':
        api_url = 'https://dapi.kakao.com/v2/search/image'
    elif search_type == 'vclip':
        api_url = 'https://dapi.kakao.com/v2/search/vclip'
    else:
        return "Invalid search type", 400
    
    params = {
        "query": query,
        "sort": "accuracy",
        "page": 1,
        "size": 10
    }
    
    results = call_kakao_api(api_url, params)
    return render_template('results.html', query=query, results=results, search_type=search_type)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
