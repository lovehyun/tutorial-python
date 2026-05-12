from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        args=["--start-maximized"]
    )

    page = browser.new_page(viewport=None)

    # 네이버 IT 뉴스 섹션
    page.goto("https://news.naver.com/section/105")

    # 헤드라인 뉴스 링크들
    # headlines = page.locator(".section_article.as_headline a.sa_text_title")
    headlines = page.locator("a.sa_text_title")

    print("헤드라인 뉴스 개수:", headlines.count())

    for i in range(headlines.count()):

        news = headlines.nth(i)

        # 제목
        title = news.inner_text().strip()

        # 링크
        href = news.get_attribute("href")

        print(f"{i+1}. {title}")
        print(href)
        print("-" * 50)

    input("엔터 누르면 종료")

    browser.close()
