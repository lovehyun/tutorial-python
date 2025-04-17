# 1. 영화 랭킹 및 제목 조회

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 크롬 드라이버 경로 설정 및 headless 모드 활성화
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 웹 페이지에 접속
url = 'http://www.cine21.com/rank/boxoffice/domestic'
driver.get(url)

# 페이지 소스코드 가져오기
page_source = driver.page_source

# BeautifulSoup을 사용하여 페이지 소스코드 파싱
bs = BeautifulSoup(page_source, 'html.parser')

# boxoffice_list_content ID를 가진 div 찾기
boxoffice_list_content = bs.find('div', id='boxoffice_list_content')

# boxoffice_list_content 내의 모든 boxoffice_li 클래스를 가진 li 요소들 찾기
boxoffice_li_list = boxoffice_list_content.find_all('li', class_='boxoffice_li')

# 각 boxoffice_li에 대해 mov_name, people_num 클래스를 가진 div의 텍스트 출력
for _, boxoffice_li in enumerate(boxoffice_li_list, start=1):
    rank_span = boxoffice_li.find('span', class_='grade')
    mov_name_div = boxoffice_li.find('div', class_='mov_name')
    people_num_div = boxoffice_li.find('div', class_='people_num')

    rank = rank_span.get_text(strip=True)
    mov_name = mov_name_div.get_text(strip=True) if mov_name_div else ''
    people_num = people_num_div.get_text(strip=True) if people_num_div else ''
    print(f"순위: {rank}, 영화 제목: {mov_name}, 관객 수: {people_num}")

# 웹 드라이버 종료
driver.quit()
