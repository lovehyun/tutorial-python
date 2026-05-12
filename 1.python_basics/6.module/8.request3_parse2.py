import requests
import re

# 웹 페이지 요청
url = "https://www.example.com"
response = requests.get(url)

# HTML 문자열 파싱하여 데이터 추출
pattern = r"<h2>(.*?)</h2>"  # <h2> 태그 사이의 내용을 추출하기 위한 정규 표현식
matches = re.findall(pattern, response.text)

# 추출된 데이터 출력
for match in matches:
    print(match)
