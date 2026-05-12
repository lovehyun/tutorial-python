import requests

# 웹 페이지 요청
url = "https://www.example.com"
response = requests.get(url)

html = response.text

start_tag = "<h2>"
end_tag = "</h2>"

results = []

# 문자열 직접 탐색
start = html.find(start_tag)
end = html.find(end_tag)

# 태그 사이 내용 추출
text = html[start + len(start_tag):end]
results.append(text)

# 이미 처리한 부분 제거
html = html[end + len(end_tag):]

# 출력
for item in results:
    print(item)
