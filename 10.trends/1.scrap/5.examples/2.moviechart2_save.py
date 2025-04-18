import requests
from bs4 import BeautifulSoup
import csv
import json

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

# 결과 저장 리스트
movies = []
movies_json = []

for idx, card in enumerate(movie_cards, start=1):
    title_tag = card.select_one('div.movie-title h3')
    img_tag = card.select_one('img')
    link_tag = card.select_one('a')

    title = title_tag.text.strip() if title_tag else '제목없음'
    image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''
    detail_link = 'https://www.moviechart.co.kr' + link_tag['href'] if link_tag else ''

    print(f"{idx:2}. 제목: {title}")
    print(f"    이미지: {image_url}")
    print(f"    상세 페이지: {detail_link}")
    
    # 한 줄씩 리스트에 저장
    movies.append([title, image_url, detail_link])

    # 딕셔너리로 저장!
    movies_json.append({
        "title": title,
        "image_url": image_url,
        "detail_link": detail_link
    })

# CSV 파일로 저장
csv_filename = 'movie_chart.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['제목', '이미지URL', '상세링크'])  # 헤더
    writer.writerows(movies)

print(f"\nCSV 저장 완료: {csv_filename}")

# JSON 파일로 저장
json_filename = 'movie_chart.json'
with open(json_filename, 'w', encoding='utf-8-sig') as f:
    json.dump(movies_json, f, ensure_ascii=False, indent=4)

print(f"\nJSON 저장 완료: {json_filename}")
