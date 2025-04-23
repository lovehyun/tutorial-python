import requests

def search_music_with_lyrics(query):
    base_url = 'https://m.search.naver.com/p/csearch/content/qapirender.nhn'
    params = {
        'where': 'm',
        'key': 'LyricsSearchResult',
        'pkid': '519',
        'u1': 1,
        'u2': 3,
        'u3': '0',
        'u4': '1',
        'q': '가사검색 ' + query,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)

        # 응답 출력 확인 (디버깅용)
        print("응답 코드:", response.status_code)
        print("응답 본문 일부:", response.text[:100])
        
        # 응답 데이터 처리
        print(response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching lyrics:', error)

# 함수 호출
search_music_with_lyrics("동해물과 백두산이")
