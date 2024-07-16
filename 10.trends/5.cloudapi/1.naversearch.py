import os
import sys
import urllib.request
import json
from tabulate import tabulate

client_id = "vK8FvChKWnW1yTJOUevC" # 개발자센터에서 발급받은 Client ID 값
client_secret = open("secret.txt", "r").read() # 개발자센터에서 발급받은 Client Secret 값

text = "Python 개발"

encText = urllib.parse.quote(text)
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

response = urllib.request.urlopen(request)

rescode = response.getcode()
if rescode == 200:
    response_body = response.read()
    print(response_body.decode('utf-8'))
    print('-'*20)

    data = json.loads(response_body)
    # print(data)
else:
    print("Error Code:" + rescode)

# 선택한 컬럼만 추출하여 리스트로 만들기
selected_columns = [["title", "link", "description"]]
for item in data["items"]:
    selected_columns.append([item["title"], item["link"], item["description"]])

# 테이블 형태로 출력
print(tabulate(selected_columns, headers="firstrow", tablefmt="list"))
