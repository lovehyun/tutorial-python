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


# 검색 결과 테이블 헤더
table_header = ['Index', 'Title', 'View Count', 'Video URL']

# 검색 결과 테이블로 출력
table = []
for index, result in enumerate(search_results, start=1):
    title = result['snippet']['title']
    video_id = result['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # videos.list를 사용하여 각 동영상의 통계 정보 가져오기
    video_params = {
        'part': 'statistics',
        'id': video_id,
        'key': API_KEY
    }
    video_response = requests.get('https://www.googleapis.com/youtube/v3/videos', params=video_params)
    video_data = video_response.json()

    # 통계 정보가 있는 경우에만 조회수 가져오기
    if 'items' in video_data and video_data['items']:
        view_count = video_data['items'][0]['statistics']['viewCount']
    else:
        view_count = 'N/A'

    table.append([index, title, view_count, video_url])  # 조회수 정보를 테이블에 추가

    # 각 동영상의 정보를 가져와서 출력
    # 헤더 출력
    # if index == 1: 
        # print(tabulate([], headers=table_header, tablefmt='plain'))
    # print(tabulate([[index, title, view_count, video_url]], tablefmt='plain'))

# 검색 결과를 테이블로 모아서 출력
print(tabulate(table, headers=['Index', 'Title', 'View Count', 'Video URL'], tablefmt='plain'))
