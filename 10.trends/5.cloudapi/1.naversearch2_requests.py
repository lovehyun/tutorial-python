import requests
import json
from tabulate import tabulate

# 네이버 API 클라이언트 ID 및 Secret 값
client_id = "vK8FvChKWnW1yTJOUevC"  # 개발자센터에서 발급받은 Client ID 값
client_secret = open("secret.txt", "r").read().strip()  # 개발자센터에서 발급받은 Client Secret 값

# 검색할 텍스트
text = "Python 개발"

# URL 인코딩
encText = requests.utils.quote(text)
url = f"https://openapi.naver.com/v1/search/blog?query={encText}"

# 요청 헤더 설정
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

# GET 요청 보내기
response = requests.get(url, headers=headers)

# 응답 코드 확인
if response.status_code == 200:
    response_body = response.text
    print(response_body)
    print('-' * 20)

    data = json.loads(response_body)
else:
    print(f"Error Code: {response.status_code}")

# 선택한 컬럼만 추출하여 리스트로 만들기
selected_columns = [["title", "link", "description"]]
for item in data["items"]:
    selected_columns.append([item["title"], item["link"], item["description"]])

# 테이블 형태로 출력
print(tabulate(selected_columns, headers="firstrow", tablefmt="list"))
