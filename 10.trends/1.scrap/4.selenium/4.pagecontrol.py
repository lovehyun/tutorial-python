# 1. 사용자 데이터 가져오기 및 DataFrame으로 변환

# 웹 페이지 열기
from selenium import webdriver

# Chrome 드라이버 초기화
driver = webdriver.Chrome()

# 웹 페이지 열기
driver.get('https://www.google.com')

# 브라우저 닫기
driver.quit()


# 2. 웹 페이지에서 요소 찾기 및 조작하기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.google.com')

# 요소 찾기
search_box = driver.find_element_by_name('q')

# 키 입력하기
search_box.send_keys('Selenium')

# 엔터키 입력하기
search_box.send_keys(Keys.RETURN)

driver.quit()
