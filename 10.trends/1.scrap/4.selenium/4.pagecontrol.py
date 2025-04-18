# 웹 페이지 열기
from selenium import webdriver
import time

# Chrome 드라이버 초기화
driver = webdriver.Chrome()

# 웹 페이지 열기
driver.get('https://www.google.com')

# 브라우저 닫기
driver.quit()


# 2. 웹 페이지에서 요소 찾기 및 조작하기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.google.com')

# 요소 찾기
# selenium3 이전 구버전 문법
# search_box = driver.find_element_by_name('q')
# selenium4 이후 문법
search_box = driver.find_element(By.NAME, "q")

# By.ID	id 속성
# By.NAME	name 속성
# By.CLASS_NAME	class 속성
# By.TAG_NAME	태그 이름 (<input>, etc.)
# By.LINK_TEXT	링크 텍스트 전체 일치
# By.PARTIAL_LINK_TEXT	링크 텍스트 일부 일치
# By.XPATH	XPath 경로
# By.CSS_SELECTOR	CSS 선택자

# 키 입력하기
search_box.send_keys('Selenium')

# 엔터키 입력하기
search_box.send_keys(Keys.RETURN)

# 또는 전송버튼 트리거
search_box.submit()

# 페이지 로딩 대기
time.sleep(2)

# 검색 결과 추출
results = driver.find_elements(By.CSS_SELECTOR, 'div.g')

print(f"검색 결과 {len(results)}개 찾음.\n")

for i, result in enumerate(results[:5], 1):  # 상위 5개만 출력
    try:
        title = result.find_element(By.TAG_NAME, "h3").text
    except:
        title = "(제목 없음)"

    try:
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = "(링크 없음)"

    try:
        snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
    except:
        snippet = "(설명 없음)"

    print(f"#{i}")
    print("제목:", title)
    print("링크:", link)
    print("설명:", snippet)
    print("-" * 60)

driver.quit()
