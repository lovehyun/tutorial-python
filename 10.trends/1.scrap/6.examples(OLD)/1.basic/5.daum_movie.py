import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.daum.net/ranking/reservation', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)  # HTML을 받아온 것을 확인할 수 있다.

# select를 이용해서, 영화 목록 가져오기
movies = soup.select('#mainContent > div > div.box_ranking > ol > li')
print(len(movies)) # 20

# 각 영화의 제목 가져오기
for movie in movies:
    # mainContent > div > div.box_ranking > ol > li:nth-child(1) > div > div.thumb_cont > strong
    title_tag = movie.select_one('div > div.thumb_cont > strong')
    if title_tag:
        movie_title = title_tag.text.strip()
        print(movie_title)

    rating_tag = movie.select_one('div > div.thumb_cont > span.txt_append > span:nth-child(1)')
    reservation_rate_tag = movie.select_one('div > div.thumb_cont > span.txt_append > span:nth-child(2)')
    
    if rating_tag:
        movie_rating = rating_tag.text.strip()
        print("평점:", movie_rating)
    
    if reservation_rate_tag:
        reservation_rate = reservation_rate_tag.text.strip()
        print("예매율:", reservation_rate)

# 각 영화의 설명 가져오기
for movie in movies:
    # 영화의 포스터 이동 링크 URL과 쇼트 설명문 가져오기
    movie_selected = movie.select_one('div > div.thumb_item > div.poster_info > a')

    if movie_selected:
        poster_link_url = movie_selected['href']
        print("포스터 이동 링크 URL:", poster_link_url)
        
        short_description = movie_selected.text.strip()
        print("영화 쇼트 설명문:", short_description)
        
