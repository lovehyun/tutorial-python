import os
import time
import base64
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
search_box.send_keys("apple fruit")

# 엔터 키 누르기 (검색 실행)
search_box.send_keys(Keys.RETURN)

# 페이지 로딩을 위해 잠시 대기
time.sleep(2)

# 스크롤하면서 이미지 다운로드
num_scrolls = 10 # 스크롤할 횟수
image_count = 0
scroll_pause_time = 2

# 마지막 스크롤 위치 초기화
last_height = driver.execute_script("return document.body.scrollHeight")


for _ in range(num_scrolls):
    # 스크롤 이벤트 발생
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)  # 스크롤 후 잠시 대기

    # 현재 페이지의 이미지 요소들 가져오기
    image_elements = driver.find_elements(By.XPATH, '//img[@class="YQ4gaf"]')[image_count:]

    # 이미지 다운로드
    for element in image_elements[:30]: # 30개씩만 다운로드
        try:
            # 이미지 데이터 추출
            image_data = element.get_attribute('src') or element.get_attribute('data-src')
            if image_data:
                if 'data:' in image_data:
                    # 이미지 헤더 확인
                    image_header = image_data.split(",")[0]
                    print('이미지 헤더: ', image_header)

                    if image_header == 'data:image/jpeg;base64':
                        # 데이터 URL에서 이미지 데이터 추출
                        image_data = image_data.split(",")[1]

                        # 이미지 데이터 디코딩
                        image_binary = base64.b64decode(image_data)
                    else:
                        image_binary = None
                else:
                    # 실제 URL로부터 이미지 다운로드
                    print('이미지 링크: ', image_data)
                    image_binary = requests.get(image_data).content
                
                # 이미지 저장
                image_count += 1
                if image_binary is not None:
                    with open(f'images/image_{image_count}.jpg', 'wb') as f:
                        f.write(image_binary)
                    print(f"Image {image_count} downloaded successfully.")
                else:
                    print(f"Image {image_count} downloaded unsuccessfully.")

        except Exception as e:
            print(f"Failed to download image {image_count}: {e}")

    # 새로운 스크롤 위치
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break  # 더 이상 스크롤할 수 없을 때 종료
    last_height = new_height

# 웹 드라이버 종료
driver.quit()
