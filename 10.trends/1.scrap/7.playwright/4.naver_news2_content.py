from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        args=["--start-maximized"]
    )

    page = browser.new_page(viewport=None)

    # 뉴스 섹션 이동
    page.goto("https://news.naver.com/section/105")

    # 뉴스 목록 가져오기
    items = page.locator("a.sa_text_title")

    # 링크 저장
    links = []

    for i in range(items.count()):

        item = items.nth(i)

        title = item.inner_text()

        href = item.get_attribute("href")

        links.append({
            "title": title,
            "href": href
        })

    # 기사 하나씩 방문
    for news in links:

        print("=" * 80)
        print("제목:", news["title"])
        print("링크:", news["href"])
        print("=" * 80)

        # 기사 페이지 이동
        page.goto(news["href"])

        # 본문 대기
        page.wait_for_selector("#dic_area")

        # 본문 추출
        content = page.locator("#dic_area").inner_text()

        print(content[:1000])  # 너무 길어서 일부만 출력

        print("\n\n")

    input("엔터 누르면 종료")

    browser.close()
