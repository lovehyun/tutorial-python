import requests

# GitHub API 엔드포인트 URL
url = 'https://api.github.com/users/lovehyun/repos'

# API로부터 데이터 가져오기
response = requests.get(url)
data = response.json()

# 1. 데이터 파싱 및 출력
for repo in data:
    name = repo['name']
    html_url = repo['html_url']
    description = repo['description']
    print(f"Repository Name: {name}")
    print(f"URL: {html_url}")
    print(f"Description: {description}")
    print('-' * 40)

# 2. 데이터 파싱 및 출력
print(f"{'Name':<30} {'Full Name':<50} {'Private':<10}")
print('-' * 90)

for repo in data:
    name = repo['name']
    full_name = repo['full_name']
    private = repo['private']
    print(f"{name:<30} {full_name:<50} {str(private):<10}")
