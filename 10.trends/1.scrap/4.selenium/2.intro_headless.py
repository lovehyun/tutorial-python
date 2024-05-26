from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

# ChromeOptions를 사용하여 headless 모드로 설정
options = Options()
options.add_argument('--headless')
# options.add_argument('--window-size=1920,1080')  # 원하는 해상도로 설정 (기본값 800x600)


# 크롬 드라이버 생성 및 headless 모드 설정
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Google 검색 페이지 열기
driver.get("https://www.google.com")

# 검색 입력창 찾기 (검색창의 이름이 'q')
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys("Python programming")

# 엔터 키 누르기 (검색 실행)
search_box.submit()

# 페이지 로딩을 위해 잠시 대기
time.sleep(2)

# 결과 페이지 스크린샷 저장
driver.save_screenshot('search_results2.png')

# 웹 드라이버 종료
driver.quit()
