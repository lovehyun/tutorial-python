import requests
import re
import json
from bs4 import BeautifulSoup

def search_lyrics_with_details(query):
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
        content = response.text.strip()

        # 정규식으로 JSONP 중 괄호 안 JSON만 추출
        match = re.search(r'^dummy\((.*)\)\s*;?\s*$', content, re.DOTALL)
        if not match:
            print("JSONP 파싱 실패. 응답 내용:\n", content[:300])
            return

        json_str = match.group(1)
        data = json.loads(json_str)

        html = data.get("current", {}).get("html", "")
        soup = BeautifulSoup(html, 'html.parser')

        results = []
        for li in soup.select("li._li"):
            title = li.select_one(".music_title a")
            singer = li.select_one(".sub_text")
            lyrics = li.select_one("p.lyrics")

            if title and singer and lyrics:
                results.append({
                    "title": title.get_text(strip=True),
                    "link": title["href"],
                    "singer": singer.get_text(strip=True),
                    "lyrics": lyrics.get_text(separator="\n", strip=True)
                })

        for idx, song in enumerate(results, 1):
            print(f"\n[{idx}] {song['title']} - {song['singer']}")
            print(f"링크: {song['link']}")
            print(f"가사:\n{song['lyrics'][:300]}...\n")

    except Exception as e:
        print("에러 발생:", e)

# 실행
if __name__ == "__main__":
    search_lyrics_with_details("동해물과 백두산이")
