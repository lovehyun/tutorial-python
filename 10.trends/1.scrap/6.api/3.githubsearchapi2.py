import requests

# GitHub 검색 API 엔드포인트 URL
url = 'https://api.github.com/search/repositories'

# 검색할 키워드
keyword = 'python scraping'

# 검색 결과를 저장할 리스트
all_repositories = []

# 최대 검색 페이지 수
max_pages = 3

for page in range(1, max_pages + 1):
    # API 쿼리 파라미터 설정 - 한번에 최대 30개
    params = {
        'q': keyword,
        'page': page
    }

    # API로부터 데이터 가져오기
    response = requests.get(url, params=params)
    data = response.json()

    # 검색 결과 확인
    if 'items' in data:
        repositories = data['items']
        all_repositories.extend(repositories)
    else:
        print("No repositories found on page", page)
        break

# 모든 검색 결과 출력
for index, repo in enumerate(all_repositories, start=1):
    name = repo['name']
    full_name = repo['full_name']
    html_url = repo['html_url']
    description = repo['description']

    print(f"Index: {index}")
    print(f"Repository Name: {name}")
    print(f"Full Name: {full_name}")
    print(f"URL: {html_url}")
    print(f"Description: {description}")
    print('-' * 40)
