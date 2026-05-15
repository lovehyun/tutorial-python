import csv
import requests

from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()

# API 키 가져오기
API_KEY = os.getenv("YOUTUBE_API_KEY")

# 검색 API 주소
url = "https://www.googleapis.com/youtube/v3/search"

# 검색 파라미터
params = {
    "part": "snippet",
    "q": "python scraping",
    "type": "video",
    "maxResults": 5,
    "key": API_KEY
}

# API 요청
response = requests.get(url, params=params)

# JSON 데이터 변환
data = response.json()

# CSV 저장
with open("search_result.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # 헤더 작성
    writer.writerow(["video_id", "title"])
    
    # 검색 결과 저장
    for item in data["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        writer.writerow([video_id, title])

print("search_result.csv 저장 완료")
