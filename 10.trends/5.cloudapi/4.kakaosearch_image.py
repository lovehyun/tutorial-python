import requests
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 카카오 API REST 키
rest_api_key = os.getenv("KAKAO_RESTAPI_KEY")

# 검색할 텍스트
query = "설현"

# API 요청 URL 및 헤더 설정
url = "https://dapi.kakao.com/v2/search/image"
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
        collection = item["collection"]
        thumbnail_url = item["thumbnail_url"]
        image_url = item["image_url"]
        width = item["width"]
        height = item["height"]
        display_sitename = item["display_sitename"]
        doc_url = item["doc_url"]
        datetime = item["datetime"]
        print(f"Collection: {collection}")
        print(f"Thumbnail URL: {thumbnail_url}")
        print(f"Image URL: {image_url}")
        print(f"Width: {width}")
        print(f"Height: {height}")
        print(f"Display Sitename: {display_sitename}")
        print(f"Document URL: {doc_url}")
        print(f"Datetime: {datetime}")
        print('-' * 40)
else:
    print(f"Error Code: {response.status_code}")
