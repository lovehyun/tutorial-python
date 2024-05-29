# pip install python-dotenv

import os
import requests
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# .env 파일에서 API_KEY 읽어오기
API_KEY = os.getenv('API_KEY')

# YouTube Data API 엔드포인트 및 검색 쿼리 설정
search_query = 'Python programming'
url = 'https://www.googleapis.com/youtube/v3/search'

# API 요청 파라미터 설정
# part 파라미터값
#  - snippet: 검색 결과에 대한 기본 정보를 포함하는 부분으로, 각 동영상의 제목, 설명, 썸네일 이미지 URL 등을 반환합니다.
#  - id: 각 동영상의 고유한 식별자만을 반환합니다.
#  - contentDetails: 동영상의 길이나 형식과 같은 추가 정보를 반환합니다.
#  - statistics: 동영상의 조회수, 좋아요 수, 싫어요 수 등의 통계 정보를 반환합니다.
#  - topicDetails: 동영상의 주제 및 카테고리와 관련된 정보를 반환합니다.
#  - snippet, id: snippet 및 id 정보를 모두 반환합니다.
#  - snippet, contentDetails: snippet 및 contentDetails 정보를 모두 반환합니다.
#  - snippet, statistics: snippet 및 statistics 정보를 모두 반환합니다.
#  - snippet, topicDetails: snippet 및 topicDetails 정보를 모두 반환합니다.
params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 10, # 최대값 50
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
