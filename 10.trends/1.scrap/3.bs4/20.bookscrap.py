import requests
from bs4 import BeautifulSoup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/?utm_source=chatgpt.com

# 웹 페이지 요청
url = "https://books.toscrape.com/"
response = requests.get(url)

# HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# find()	   태그 기반 탐색
# find_all()   여러 개
# select()	   CSS 선택자 기반
# select_one() 첫 번째 요소

# 책 목록 가져오기
books = soup.select("article.product_pod")

# 출력
for book in books:
    # 도서명
    title = book.h3.a["title"]

    # 가격
    price = book.select_one(".price_color").text

    # 평점
    rating = book.p["class"][1]

    print(f"도서명: {title}")
    print(f"가격: {price}")
    print(f"평점: {rating}")
    print("-" * 30)


# find()	태그 기반 탐색
# soup.find("div", class_="title")
# soup.find("div", id="main")
# soup.find_all("a")
# book.find("h3").find("a")
# title = book.find("h3").find("a")["title"]

# select()	CSS 선택자 기반
# soup.select("h1")
# soup.select(".title")
# soup.select("#main")
# soup.select("div a") # div 안의 모든 a
# book.select_one("h3 a")
# title = book.select_one("h3 a")["title"]
