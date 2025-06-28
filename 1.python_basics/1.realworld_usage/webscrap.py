# 웹 스크래핑: 인터넷에서 웹 페이지의 데이터를 추출하는 기술
import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
url = "https://www.example.com"
response = requests.get(url)

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 데이터 추출
title = soup.title.text
print("웹 페이지 제목:", title)
