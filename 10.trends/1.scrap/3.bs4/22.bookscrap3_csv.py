import requests
from bs4 import BeautifulSoup
import csv

# 웹 페이지 요청
url = "https://books.toscrape.com/"
response = requests.get(url)

# UTF-8 인코딩 지정
response.encoding = "utf-8"

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 평점 변환용 딕셔너리
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# 책 목록 가져오기
books = soup.select("article.product_pod")

# CSV 저장
with open("books.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    # 헤더 작성
    writer.writerow(["도서명", "가격", "평점"])

    # 데이터 작성
    for book in books:
        # 도서명
        title = book.h3.a["title"]

        # 가격
        price_text = book.select_one(".price_color").text
        price = price_text.replace("Â£", "").replace("£", "")

        # 평점
        rating_text = book.p["class"][1]
        rating = rating_map[rating_text]

        # CSV 한 줄 저장
        writer.writerow([title, price, rating])

print("books.csv 저장 완료")
