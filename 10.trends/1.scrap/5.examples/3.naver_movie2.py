from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 크롬 드라이버 경로 설정 및 headless 모드 활성화
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# 크롬 드라이버 생성
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 웹 페이지에 접속
url = 'https://serieson.naver.com/v3/movie/ranking/realtime'
driver.get(url)

# 페이지 로딩 대기
driver.implicitly_wait(2)  # 암묵적 대기

def get_movie_list(movie_list):
    for rank, movie in enumerate(movie_list, start=1):
        # print(movie.text)

        print(f"{rank:2d}: ", end="")

        a_movie = movie.find_element(By.CSS_SELECTOR, 'span.Title_title__s9o0D')
        print(f"{a_movie.text} ", end="")

        link = movie.find_element(By.TAG_NAME, 'a')
        print(link.get_attribute('href'))


# 기본 "영화" 링크를 기반으로 "영화 목록" 추출
# boxoffice_list_content 적절한 ID를 가진 div 찾기
movie_list = driver.find_elements(By.XPATH, '//*[@id="container"]/div[2]/ol/li')

get_movie_list(movie_list)

print("-" * 50)

# "방송" 링크 클릭
broadcast_link = driver.find_element(By.XPATH, "//a[contains(@href, '/v3/broadcasting/ranking/realtime')]")
broadcast_link.click()

# 페이지 로딩 대기
driver.implicitly_wait(2)  # 암묵적 대기
movie_list = driver.find_elements(By.XPATH, '//*[@id="container"]/div[2]/ol/li')

get_movie_list(movie_list)
