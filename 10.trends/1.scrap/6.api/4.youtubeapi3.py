import os
import requests
from dotenv import load_dotenv
from tabulate import tabulate

# 환경 변수 로드
load_dotenv()

# API 키 설정
API_KEY = os.getenv('YOUTUBE_API_KEY')

# YouTube Data API 엔드포인트 설정
url = 'https://www.googleapis.com/youtube/v3/search'

# 검색 쿼리 설정
search_query = 'Python programming'

# 페이지별 최대 결과 수와 페이지 수 설정
max_results_per_page = 10
total_pages = 5

# 검색 결과를 저장할 리스트
search_results = []

# 각 페이지별로 요청하여 검색 결과 저장
for page in range(1, total_pages + 1):
    params = {
        'part': 'snippet',
        'q': search_query,
        'type': 'video',
        'maxResults': max_results_per_page,
        'pageToken': None if page == 1 else next_page_token,
        'key': API_KEY
    }
    
    # API 요청 보내기
    response = requests.get(url, params=params)
    data = response.json()

    # 검색 결과 파싱하여 저장
    search_results.extend(data['items'])
    
    # 다음 페이지 토큰 저장
    next_page_token = data.get('nextPageToken')

# 검색 결과 테이블로 출력
table = []
# for result in search_results:
for index, result in enumerate(search_results, start=1):
    title = result['snippet']['title']
    video_id = result['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    # table.append([title, video_url])
    table.append([index, title, video_url])

# print(tabulate(table, headers=['Title', 'Video URL'], tablefmt='plain')) # plain, simple, grid, pipe
print(tabulate(table, headers=['Index', 'Title', 'Video URL'], tablefmt='plain'))
