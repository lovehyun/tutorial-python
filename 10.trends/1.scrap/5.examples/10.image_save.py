import os
import time
import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


# 이미지를 저장할 폴더 생성
if not os.path.exists('images'):
    os.makedirs('images')

# 크롬 드라이버 생성 (자동관리)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(3)

# Google 이미지 검색 페이지 열기
driver.get("https://www.google.com/imghp")

# 검색 입력창 찾기
search_box = driver.find_element(By.NAME, 'q')

# 검색어 입력
search_box.send_keys("apple")

# 엔터 키 누르기 (검색 실행)
search_box.send_keys(Keys.RETURN)

# 페이지 로딩을 위해 잠시 대기
time.sleep(2)

# 이미지 URL 추출
image_elements = driver.find_elements(By.XPATH, '//img[@class="YQ4gaf"]')

# 처음 30개의 이미지 요소만 사용
image_elements = image_elements[:30]

# 이미지 다운로드
for i, element in enumerate(image_elements, start=1):
    try:
        # 이미지 데이터 추출
        image_data = element.get_attribute('src')
        # 데이터 URL에서 이미지 데이터 추출
        image_data = image_data.split(",")[1]
        # 이미지 데이터 디코딩
        image_binary = base64.b64decode(image_data)
        # 이미지 저장
        with open(f'images/image_{i}.jpg', 'wb') as f:
            f.write(image_binary)
        print(f"Image {i} downloaded successfully.")
    except Exception as e:
        print(f"Failed to download image {i}: {e}")

# 웹 드라이버 종료
driver.quit()
