import requests
from bs4 import BeautifulSoup

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

# 출력
for book in books:
    # 도서명
    title = book.h3.a["title"]

    # 가격 (£ 및 이상한 문자 제거)
    price_text = book.select_one(".price_color").text
    price = price_text.replace("Â£", "").replace("£", "")

    # 평점 문자열 → 숫자 변환
    rating_text = book.p["class"][1]
    rating = rating_map[rating_text]

    print(f"도서명: {title}")
    print(f"가격: {price}")
    print(f"평점: {rating}")
    print("-" * 30)
