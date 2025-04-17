import sqlite3
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# 접속
base_url = 'http://www.cine21.com'
ranking_url = base_url + '/rank/boxoffice/domestic'
driver.get(ranking_url)
driver.implicitly_wait(2)

# DB 연결 및 테이블 생성
conn = sqlite3.connect('movies.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER,
    title TEXT,
    audience TEXT,
    detail_link TEXT,
    poster_url TEXT,
    poster_blob BLOB,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(title, audience)
)
''')
conn.commit()

# 이미지 다운로드 함수
def download_image_as_blob(img_url):
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            return response.content  # BLOB 저장용
    except Exception as e:
        print("이미지 다운로드 실패:", e)
    return None

# 영화 정보 추출 함수
def get_movie_lists():
    boxoffice_list_content = driver.find_element(By.CSS_SELECTOR, 'div#boxoffice_list_content')
    boxoffice_li_list = boxoffice_list_content.find_elements(By.CSS_SELECTOR, 'li.boxoffice_li')

    for boxoffice_li in boxoffice_li_list:
        rank = int(boxoffice_li.find_element(By.CSS_SELECTOR, 'span.grade').text.strip())
        title = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.mov_name').text.strip()
        audience = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.people_num').text.strip()
        detail_link = base_url + boxoffice_li.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # 이미지 URL 추출
        try:
            poster_img = boxoffice_li.find_element(By.CSS_SELECTOR, 'img')
            poster_url = poster_img.get_attribute('src')
            poster_blob = download_image_as_blob(poster_url)
        except:
            poster_url = ''
            poster_blob = None

        print(f"순위: {rank}, 제목: {title}, 관객: {audience}, 이미지: {poster_url}")

        # DB 삽입 (중복이면 무시)
        cur.execute('''
        INSERT OR IGNORE INTO movies (rank, title, audience, detail_link, poster_url, poster_blob)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (rank, title, audience, detail_link, poster_url, poster_blob))

    conn.commit()

# 첫 페이지
get_movie_lists()

# 2~10페이지 반복
for page in range(2, 11):
    print(f"\n== {page}페이지 이동 중 ==")
    page_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.page a")))

    if page <= len(page_links):
        page_links[page - 1].click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#boxoffice_list_content li.boxoffice_li')))
        time.sleep(1.5)
        get_movie_lists()

# 마무리
driver.quit()
conn.close()
