import csv
import requests

from dotenv import load_dotenv
import os

from datetime import datetime

# .env 로드
load_dotenv()

# API 키
API_KEY = os.getenv("YOUTUBE_API_KEY")

# -----------------------------------
# CSV에서 video_id 읽기
# -----------------------------------

video_ids = []

with open("search_result.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        video_ids.append(row["video_id"])

# -----------------------------------
# videos.list 요청
# -----------------------------------

url = "https://www.googleapis.com/youtube/v3/videos"

params = {
    "part": "snippet,statistics",
    "id": ",".join(video_ids),
    "key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

# -----------------------------------
# append 저장
# -----------------------------------

file_exists = os.path.exists("video_stats.csv")

with open("video_stats.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # 파일이 없으면 헤더 작성
    if not file_exists:
        writer.writerow([
            "collected_at",
            "video_id",
            "title",
            "view_count",
            "like_count",
            "comment_count"
        ])

    # 현재 수집 시간
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 저장
    for item in data["items"]:
        video_id = item["id"]
        title = item["snippet"]["title"]
        stats = item["statistics"]
        view_count = stats.get("viewCount", 0)
        like_count = stats.get("likeCount", 0)
        comment_count = stats.get("commentCount", 0)

        writer.writerow([
            collected_at,
            video_id,
            title,
            view_count,
            like_count,
            comment_count
        ])

        print(title)
        print("조회수:", view_count)
        print("-" * 50)

print("video_stats.csv append 완료")
