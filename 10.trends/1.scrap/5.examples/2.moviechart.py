import requests
from bs4 import BeautifulSoup

URL = 'https://www.moviechart.co.kr/rank/realtime/index/image'
headers = {
    'User-Agent': 'Mozilla/5.0'  # 일부 사이트는 UA 없으면 차단함
}

# HTML 가져오기
response = requests.get(URL, headers=headers)
response.raise_for_status()  # 오류 발생 시 예외 발생
soup = BeautifulSoup(response.text, 'html.parser')

# 영화 카드 선택자
movie_cards = soup.select('div.movieBox li.movieBox-item')
print('무비카드 개수: ', len(movie_cards))

for idx, card in enumerate(movie_cards, start=1):
    title_tag = card.select_one('div.movie-title h3')
    img_tag = card.select_one('img')
    link_tag = card.select_one('a')

    title = title_tag.text.strip() if title_tag else '제목없음'
    image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''
    detail_link = 'https://www.moviechart.co.kr' + link_tag['href'] if link_tag else ''

    print(f"{idx:2}. 제목: {title}")
    print(f"    이미지: {image_url}")
    print(f"    링크: {detail_link}")
    print(f"    상세 페이지: {detail_link}")
