import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
url = "https://www.example.com"
response = requests.get(url)

# 응답 내용을 BeautifulSoup으로 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 제목과 링크 추출
titles = soup.find_all("h2")  # h2 태그를 가진 모든 요소 추출

for title in titles:
    link = title.a  # 태그 내의 링크 요소 추출
    if link:
        title_text = link.text  # 제목 텍스트 추출
        href = link.get("href")  # 링크 URL 추출
        print(f"제목: {title_text}")
        print(f"링크: {url}{href}")
        print()
