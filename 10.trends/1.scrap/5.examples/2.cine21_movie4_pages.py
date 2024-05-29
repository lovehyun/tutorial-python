# 2. 페이지 반복하며 10페이지 모두다 조회

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


# 크롬 드라이버 경로 설정 및 headless 모드 활성화
options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 웹 페이지에 접속
url = 'http://www.cine21.com/rank/boxoffice/domestic'
driver.get(url)

# 페이지 로딩을 위해 적정시간 대기
driver.implicitly_wait(2)

# 페이지 로딩 대기 변수 정의
wait = WebDriverWait(driver, 10)

def get_movie_lists():
    # boxoffice_list_content ID를 가진 div 찾기
    boxoffice_list_content = driver.find_element(By.CSS_SELECTOR, 'div#boxoffice_list_content')

    # boxoffice_list_content 내의 모든 boxoffice_li 클래스를 가진 li 요소들 찾기
    boxoffice_li_list = boxoffice_list_content.find_elements(By.CSS_SELECTOR, 'li.boxoffice_li')

    # 각 boxoffice_li에 대해 mov_name, people_num 클래스를 가진 div의 텍스트 출력
    for _, boxoffice_li in enumerate(boxoffice_li_list, start=1):
        rank_span = boxoffice_li.find_element(By.CSS_SELECTOR, 'span.grade')
        mov_name_div = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.mov_name')
        people_num_div = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.people_num')

        rank = rank_span.text.strip()
        mov_name = mov_name_div.text.strip() if mov_name_div else ''
        people_num = people_num_div.text.strip() if people_num_div else ''
        print(f"순위: {rank}, 영화 제목: {mov_name}, 관객 수: {people_num}")


# 첫 페이지 가져오기
get_movie_lists()

# 두번째 페이지 및 반복적으로 가져오기
for page in range(2, 11):
    # page_a_tags = driver.find_elements(By.CSS_SELECTOR, "div.page a")
    page_a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.page a")))
    
    # 다음 페이지 링크 클릭 (첫 번째 요소는 현재 페이지를 가리키므로 제외)
    if page <= len(page_a_tags):
        print('-' * 50)
        print(f"Clicking {page}th page link")
        page_a_tags[page - 1].click()
        
        # 페이지 로딩 대기
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#boxoffice_list_content li.boxoffice_li')))
        time.sleep(2)
        
        # 영화 리스트 가져오기
        get_movie_lists()
        
# 웹 드라이버 종료
driver.quit()
