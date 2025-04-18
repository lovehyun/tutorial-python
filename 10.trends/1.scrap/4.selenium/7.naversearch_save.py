# pip install selenium
# pip install webdriver_manager
# pip install beautifulsoup4

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import csv

# 브라우저 실행
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# 네이버 접속 및 검색
driver.get('https://www.naver.com')
search_box = driver.find_element(By.NAME, 'query')
search_box.send_keys("Python programming")
search_box.submit()

# 검색 결과 기다리기
time.sleep(3)

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 결과 저장용 리스트
book_list = []

# 각 책 항목을 감싸는 li.item 요소 기준으로 탐색
book_items = soup.select("li.item._slog_visible")

for item in book_items:
    # 제목과 링크
    a_tag = item.select_one("a.item_title")
    title = a_tag.text.strip() if a_tag else "(제목 없음)"
    link = a_tag["href"] if a_tag else "(링크 없음)"

    # 가격 추출
    price_tag = item.select_one("span.price em.strong")
    price = price_tag.text.strip() + "원" if price_tag else "가격 없음"

    # 결과 저장 및 출력
    book_list.append([title, link, price])
    print(f"제목: {title}\n링크: {link}\n가격: {price}\n" + "-"*50)

# 브라우저 종료
driver.quit()

# CSV 저장
csv_filename = "naver_books.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["제목", "링크", "가격"])  # 헤더
    writer.writerows(book_list)

print(f"CSV 저장 완료: {csv_filename}")
