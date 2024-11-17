import requests
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 카카오 API REST 키
rest_api_key = os.getenv("KAKAO_RESTAPI_KEY")

# 검색할 텍스트
query = "AOA"

# API 요청 URL 및 헤더 설정
url = "https://dapi.kakao.com/v2/search/vclip"
headers = {
    "Authorization": f"KakaoAK {rest_api_key}"
}

# 요청 파라미터 설정
params = {
    "query": query,
    "sort": "accuracy",  # 정확도순 정렬
    "page": 1,           # 페이지 번호
    "size": 10           # 한 페이지에 보여질 문서 수
}

# GET 요청 보내기
response = requests.get(url, headers=headers, params=params)

# 응답 코드 확인
if response.status_code == 200:
    data = response.json()
    
    # 검색 결과 출력
    print(f"Total Count: {data['meta']['total_count']}")
    print(f"Pageable Count: {data['meta']['pageable_count']}")
    print(f"Is End: {data['meta']['is_end']}")
    print('-' * 40)

    # 검색 결과 문서 출력
    for item in data["documents"]:
        title = item["title"].replace("<b>", "").replace("</b>", "")
        url = item["url"]
        play_time = item["play_time"]
        thumbnail = item["thumbnail"]
        datetime = item["datetime"]
        author = item["author"]
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Play Time: {play_time} seconds")
        print(f"Thumbnail: {thumbnail}")
        print(f"Datetime: {datetime}")
        print(f"Author: {author}")
        print('-' * 40)
else:
    print(f"Error Code: {response.status_code}")
