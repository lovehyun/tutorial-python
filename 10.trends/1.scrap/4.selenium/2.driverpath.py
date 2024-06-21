from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# ChromeDriver 경로 설정
chromedriver_path = "path/to/your/chromedriver"  # chromedriver 경로 설정
# chromedriver_path = "C:\\devs\\bin\\chromedriver.exe"

# ChromeDriver 서비스 설정
service = Service(executable_path=chromedriver_path)

# 브라우저 드라이버 생성
driver = webdriver.Chrome(service=service)

# 웹 페이지 열기
driver.get('https://www.google.com')

# 브라우저 닫기
driver.quit()
