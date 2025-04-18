import os
import json
import sys
import urllib.request
from dotenv import load_dotenv
from tabulate import tabulate

# .env 파일에서 환경 변수 로딩
load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

text = "Python 개발"
encText = urllib.parse.quote(text)
url = "https://openapi.naver.com/v1/search/blog?query=" + encText

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

response = urllib.request.urlopen(request)
rescode = response.getcode()

if rescode == 200:
    response_body = response.read()
    data = json.loads(response_body)
else:
    print("Error Code:", rescode)
    sys.exit(1)

# 출력
selected_columns = [["title", "link", "description"]]
for item in data["items"]:
    selected_columns.append([item["title"], item["link"], item["description"]])

print(tabulate(selected_columns, headers="firstrow", tablefmt="list"))
