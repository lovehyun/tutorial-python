from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Headless 옵션 설정
options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 드라이버 실행
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 위키 문서 접속
driver.get("https://en.wikipedia.org/wiki/Python_(programming_language)")
time.sleep(2)  # 페이지 로딩 대기

# 제목
title = driver.find_element(By.ID, "firstHeading").text
print("제목:", title)

# 첫 문단 (내용 있는 첫 p)
paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
first_paragraph = ""
for p in paragraphs:
    if p.text.strip():
        first_paragraph = p.text.strip()
        break
print("\n첫 문단:\n", first_paragraph)

# 목차 항목
print("\n목차:")
try:
    toc_items = driver.find_elements(By.CSS_SELECTOR, "div#vector-toc ul.vector-toc-contents > li.vector-toc-list-item")
    if toc_items:
        for item in toc_items:
            text = item.find_element(By.CSS_SELECTOR, "div.vector-toc-text").text.strip()
            print("-", text)
    else:
        print("목차 항목이 없습니다.")
except:
    print("목차를 찾을 수 없습니다.")
    
driver.quit()
