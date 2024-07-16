import requests
from datetime import datetime, timedelta

# GitHub API 엔드포인트 URL
url = 'https://api.github.com/users/lovehyun/repos'

# API로부터 데이터 가져오기
response = requests.get(url)
data = response.json()

# 현재 날짜와 한 달 전 날짜 계산
today = datetime.utcnow()
one_month_ago = today - timedelta(days=30)
one_month_ago_iso = one_month_ago.isoformat() + 'Z'

# 1. 데이터 파싱 및 상세 정보 출력
print(f"{'Name':<20} {'URL':<50} {'Description':<30} {'Owner':<20} {'Language':<15} {'Stars':<7} {'Forks':<7} {'Default Branch':<15} {'Created At':<25} {'Updated At':<25}")
print('-' * 180)

for repo in data:
    name = repo['name']
    html_url = repo['html_url']
    description = repo['description'] or ""
    owner = repo['owner']['login']
    language = repo['language'] or "N/A"
    stargazers_count = repo['stargazers_count']
    forks_count = repo['forks_count']
    default_branch = repo['default_branch']
    created_at = repo['created_at']
    updated_at = repo['updated_at']
    print(f"{name:<20} {html_url:<50} {description:<30} {owner:<20} {language:<15} {stargazers_count:<7} {forks_count:<7} {default_branch:<15} {created_at:<25} {updated_at:<25}")

# 2. 특정 필드별로 데이터를 그룹화하여 출력
print("\n스타가 많은 레포지토리들:")
star_threshold = 50
for repo in data:
    if repo['stargazers_count'] > star_threshold:
        name = repo['name']
        stargazers_count = repo['stargazers_count']
        print(f"{name}: {stargazers_count} stars")

print("\n최근 한 달간 업데이트된 레포지토리들:")
for repo in data:
    if repo['updated_at'] > one_month_ago_iso:
        name = repo['name']
        updated_at = repo['updated_at']
        print(f"{name}: Last updated at {updated_at}")
