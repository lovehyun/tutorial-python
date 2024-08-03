import requests

# GitHub 검색 API 엔드포인트 URL
url = 'https://api.github.com/search/repositories'

# 검색할 키워드
keyword = 'python scraping'

# API 쿼리 파라미터 설정
params = {
    'q': keyword
}

# API로부터 데이터 가져오기 - 한번에 최대 30개 반환함
response = requests.get(url, params=params)
data = response.json()

# 검색 결과 확인
if 'items' in data:
    repositories = data['items']
    # 검색된 저장소 순회하며 출력
    for repo in repositories:
        name = repo['name']
        full_name = repo['full_name']
        html_url = repo['html_url']
        description = repo['description']
        
        print(f"Repository Name: {name}")
        print(f"Full Name: {full_name}")
        print(f"URL: {html_url}")
        print(f"Description: {description}")
        print('-' * 40)
else:
    print("No repositories found.")
