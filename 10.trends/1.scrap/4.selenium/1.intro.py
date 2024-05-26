# Selenium 라이브러리 설치: pip install selenium
# 크롬 드라이버 자동관리: pip install webdriver_manager

# 수동 관리 시 아래 참고, 웹드라이버통한 자동 관리 시 불필요
# https://developer.chrome.com/docs/chromedriver/get-started?hl=ko
# https://googlechromelabs.github.io/chrome-for-testing/#stable

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# 크롬 드라이버 생성 (수동실행, chromedriver.exe 의 PATH 추가 필요)
# driver = webdriver.Chrome()

# Google 검색 페이지 열기
driver.get("https://www.google.com")

# 검색 입력창 찾기 (검색창의 이름이 'q')
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys("Python programming")

# 엔터 키 누르기 (검색 실행)
search_box.submit()

# 페이지 로딩을 위해 잠시 대기
time.sleep(5)

# 결과 페이지 스크린샷 저장
driver.save_screenshot('search_results.png')

# 웹 드라이버 종료
driver.quit()
