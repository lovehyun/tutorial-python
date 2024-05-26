# https://developers.google.com/youtube/v3/docs/search/list

import requests

# YouTube Data API 엔드포인트 및 API 키
API_KEY = 'YOUR_API_KEY'  # 실제 API 키로 바꾸세요.
search_query = 'Python programming'
url = 'https://www.googleapis.com/youtube/v3/search'

# API 요청 파라미터 설정
params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 10,
    'key': API_KEY
}

# API 요청 보내기
response = requests.get(url, params=params)
data = response.json()

# 결과 파싱 및 출력
for item in data['items']:
    title = item['snippet']['title']
    video_id = item['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    description = item['snippet']['description']
    print(f"Title: {title}")
    print(f"URL: {video_url}")
    print(f"Description: {description}")
    print('-' * 40)
