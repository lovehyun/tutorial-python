import requests
from bs4 import BeautifulSoup
import csv

# 웹 페이지 요청
url = "https://books.toscrape.com/"
response = requests.get(url)

response.encoding = "utf-8"

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 평점 변환
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# 책 목록
books = soup.select("article.product_pod")

# CSV 저장
with open("books.csv", "w", newline="", encoding="utf-8-sig") as file:

    fieldnames = ["title", "price", "rating"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # 헤더 작성
    writer.writeheader()

    # 데이터 저장
    for book in books:

        title = book.h3.a["title"]

        price_text = book.select_one(".price_color").text
        price = price_text.replace("Â£", "").replace("£", "")

        rating_text = book.p["class"][1]
        rating = rating_map[rating_text]

        # 딕셔너리 형태로 저장
        writer.writerow({
            "title": title,
            "price": price,
            "rating": rating
        })

print("CSV 저장 완료")
