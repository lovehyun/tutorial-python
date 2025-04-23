import requests

def fetch_lyrics_raw(query):
    url = "https://m.search.naver.com/p/csearch/content/nqapirender.nhn"
    params = {
        'callback': 'dummy',
        'where': 'nexearch',
        'key': 'LyricsSearchResult',
        'pkid': '519',
        'u1': '1',
        'u2': '5',
        'u3': '1',
        'u4': '1',
        'u5': query,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        print("\n응답 받은 원본 데이터 (JSONP 형식):\n")
        print(response.text)
    except Exception as e:
        print("에러 발생:", e)

# 테스트 실행
if __name__ == "__main__":
    fetch_lyrics_raw("동해물과 백두산이")
