import requests
from bs4 import BeautifulSoup

def search_youtube(query):
    # 유튜브 검색 결과 페이지 URL
    url = f"https://www.youtube.com/results?search_query={query}"

    # HTTP GET 요청
    response = requests.get(url)

    # 응답 확인
    if response.status_code == 200:
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 검색 결과로부터 동영상 제목 가져오기
        video_titles = soup.find_all('a', class_='yt-simple-endpoint style-scope ytd-video-renderer')

        # 검색 결과 출력
        for title in video_titles:
            print(title.text.strip())
    else:
        print("요청에 실패했습니다.")

# 검색어 입력 받기
query = input("검색어를 입력하세요: ")

# 유튜브 검색 실행
search_youtube(query)
