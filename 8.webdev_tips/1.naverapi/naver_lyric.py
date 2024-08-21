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

    try:
        response = requests.get(base_url, params=params)

        # 응답 데이터 처리
        print(response.json())
    except requests.exceptions.RequestException as error:
        print('Error fetching lyrics:', error)

# 함수 호출
search_music_with_lyrics("동해물과 백두산이")
