# pip install requests tabulate python-dotenv

from dotenv import load_dotenv
from tabulate import tabulate
import os
import sys
import requests

# .env 파일에서 환경 변수 로딩
load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

text = "Python 개발"
url = "https://openapi.naver.com/v1/search/blog"

headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

params = {
    "query": text
}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print("요청 실패:", e)
    sys.exit(1)

# 출력
selected_columns = [["title", "link", "description"]]
for item in data.get("items", []):
    selected_columns.append([item["title"], item["link"], item["description"]])

print(tabulate(selected_columns, headers="firstrow", tablefmt="list"))
