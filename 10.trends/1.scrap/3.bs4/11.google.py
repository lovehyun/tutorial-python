import requests
from bs4 import BeautifulSoup

def google_search(query):
    url = "https://www.google.com/search"
    params = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # 요청이 성공했는지 확인

    # 상태 코드 확인
    # try:
    #     response.raise_for_status()  # 오류가 있는 경우 예외 발생
    # except requests.exceptions.HTTPError as e:
    #     print(f"HTTP error occurred: {e}")  # 오류 메시지 출력
    #     return None
    # except Exception as e:
    #     print(f"An error occurred: {e}")  # 다른 오류 처리
    #     return None
    

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for item in soup.select('div.g'):
        title = item.select_one('h3').text if item.select_one('h3') else ''
        link = item.select_one('a')['href'] if item.select_one('a') else ''
        snippet = item.select_one('.IsZvec').text if item.select_one('.IsZvec') else ''
        search_results.append({'title': title, 'link': link, 'snippet': snippet})

    return search_results

# 검색할 쿼리
query = "Python programming"

# 검색 수행
search_results = google_search(query)

# 검색 결과 출력
for result in search_results:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Snippet: {result['snippet']}")
    print("\n")
