import requests
from bs4 import BeautifulSoup


# 웹 페이지에 GET 요청 보내기
url = 'https://news.naver.com/section/105' # IT/과학 뉴스
response = requests.get(url)

# 응답의 텍스트를 BeautifulSoup으로 파싱
bs = BeautifulSoup(response.text, 'html.parser')

# 헤드라인 섹션 - section_article 클래스를 가진 div 태그 찾기
section_articles = bs.find_all('div', class_='section_article as_headline _TEMPLATE')
# section_articles = bs.select('div.section_article.as_headline._TEMPLATE')

# 각 section_article에 대해 sa_text_title 클래스를 가진 태그 찾아 출력
for section_article in section_articles:
    sa_text_titles = section_article.find_all('a', class_='sa_text_title')
    for sa_text_title in sa_text_titles:
        print(sa_text_title.get_text().strip())

print('-' * 50)

# 헤드라인 아래 섹션
section_articles = bs.find_all('div', class_='section_article _TEMPLATE')

for section_article in section_articles:
    sa_text_titles = section_article.find_all('a', class_='sa_text_title')
    for sa_text_title in sa_text_titles:
        print(sa_text_title.get_text().strip())
