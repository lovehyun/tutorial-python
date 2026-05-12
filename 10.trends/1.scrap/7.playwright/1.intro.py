# pip install playwright
# playwright install
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # 크롬 브라우저 실행
    browser = p.chromium.launch(headless=False)

    # 새 페이지 생성
    page = browser.new_page()

    # 사이트 접속
    page.goto("https://example.com")

    # 페이지 제목 출력
    print(page.title())

    # 스크린샷 저장
    page.screenshot(path="example.png")

    input("엔터 누르면 종료")

    # 브라우저 종료
    browser.close()
