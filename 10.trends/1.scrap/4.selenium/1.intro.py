# 환경변수에 chromedriver.exe 가 실행 가능해야 함
from selenium import webdriver

# Chrome 드라이버 초기화
driver = webdriver.Chrome()

# 웹 페이지 열기
driver.get('https://www.google.com')

# 브라우저 닫기
driver.quit()
