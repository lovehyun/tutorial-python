from selenium import webdriver

# Chrome 드라이버 초기화
driver = webdriver.Chrome('path/to/your/chromedriver')

# 웹 페이지 열기
driver.get('https://www.google.com')

# 브라우저 닫기
driver.quit()
