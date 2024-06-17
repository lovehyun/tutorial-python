import requests
from bs4 import BeautifulSoup

def naver_search(query):
    base_url = "https://search.naver.com/search.naver"
    params = {'query': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()  # 요청이 성공했는지 확인

    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.select('div.group_news > .list_news'):
        # 동적으로 그려지는 영역이라 나오지 않음...
        
        title_tag = item.select_one('.news_contents > a')
        title = title_tag.text if title_tag else ''
        link = title_tag['href'] if title_tag else ''
        description_tag = item.select_one('dd')
        description = description_tag.text if description_tag else ''
        search_results.append({'title': title, 'link': link, 'description': description})

    return search_results

# 검색할 쿼리
query = "Python programming"

# 검색 수행
search_results = naver_search(query)

# 검색 결과 출력
for result in search_results:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Description: {result['description']}")
    print("\n")
