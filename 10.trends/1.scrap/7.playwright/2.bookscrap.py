from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # 브라우저 실행
    browser = p.chromium.launch(headless=False)

    # 페이지 생성
    page = browser.new_page()

    # 사이트 접속
    page.goto("https://books.toscrape.com/")

    # 책 목록 가져오기
    books = page.locator("article.product_pod")

    # 책 개수만큼 반복
    for i in range(books.count()):

        book = books.nth(i)

        # 도서명
        title = book.locator("h3 a").get_attribute("title")

        # 가격
        price = book.locator(".price_color").inner_text()
        price = price.replace("£", "")

        # 평점
        rating = book.locator("p.star-rating").get_attribute("class")
        rating = rating.split()[-1]

        print(f"도서명: {title}")
        print(f"가격: {price}")
        print(f"평점: {rating}")
        print("-" * 30)

    input("엔터 누르면 종료")

    # 브라우저 종료
    browser.close()
