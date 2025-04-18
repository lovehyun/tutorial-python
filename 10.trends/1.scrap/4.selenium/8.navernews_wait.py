# pip install selenium webdriver-manager beautifulsoup4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 오늘의 스포츠 뉴스 (동적 콘텐츠 포함)
def get_naver_sportsnews():
    options = Options()
    options.add_argument('--headless')  # 창 없이 실행
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://sports.news.naver.com/index")

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".today_list > li"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        news_items = soup.select(".today_list > li")
        print(f"\n오늘의 뉴스 개수: {len(news_items)}\n")

        for n in news_items:
            a_tag = n.select_one("a")
            title = a_tag.get("title", "").strip() if a_tag else "(제목 없음)"
            href = a_tag.get("href", "#") if a_tag else "#"
            print(f"제목: {title}")
            print(f"링크: {href}")
            print("-" * 50)
            
            # 해당 뉴스 기사 페이지 내용을 가져오는 함수 호출
            get_news_content(href)

    finally:
        driver.quit()


def get_news_content(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        # 본문 div._article_content 가 나타날 때까지 대기
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._article_content"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 제목과 본문 추출
        headline = soup.select_one("h2")
        if headline:
            print(f"📰 Headline: {headline.text.strip()}")

        # 본문 전체 텍스트
        content = soup.select_one("div._article_content")
        if content:
            text = content.get_text(separator="\n", strip=True)
            print(f"\n📄 Content:\n{text[:200]}...\n")  # 앞 200자 출력

        # 이미지 URL 추출 (선택)
        images = soup.select("div._article_content img")
        for idx, img in enumerate(images, 1):
            img_url = img.get("src")
            print(f"이미지 {idx}: {img_url}")

    except Exception as e:
        print(f"❌ 기사 본문 로딩 실패: {e}")

    finally:
        driver.quit()
        print("-" * 80)

# 추천 뉴스 (렌더링 후 로딩되는 영역)
def get_naver_sportsnews_recommend():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://sports.news.naver.com/index")

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#_sports_home_airs_area"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        recommend_area = soup.select_one("#_sports_home_airs_area")
        news_items = recommend_area.select("li") if recommend_area else []

        print(f"\n추천 뉴스 개수: {len(news_items)}\n")
        for idx, item in enumerate(news_items, 1):
            text = item.get_text(strip=True)
            print(f"{idx}. {text}")

    except Exception as e:
        print(f"추천 뉴스 로딩 실패: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    # 뉴스 및 해당 페이지 본문
    get_naver_sportsnews()
    
    # 메인 화면의 아래쪽 동적 렌더링 되는 '추천 뉴스' 영역
    get_naver_sportsnews_recommend()
