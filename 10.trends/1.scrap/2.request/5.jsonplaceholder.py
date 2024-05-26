import requests

# API 엔드포인트 URL
url = 'https://jsonplaceholder.typicode.com/users'

# API로부터 데이터 가져오기
response = requests.get(url)
data = response.json()

# 데이터 파싱 및 출력
print(f"{'ID':<5} {'Name':<25} {'Username':<15} {'Email':<30}")
print('-' * 75)

for user in data:
    id = user['id']
    name = user['name']
    username = user['username']
    email = user['email']
    print(f"{id:<5} {name:<25} {username:<15} {email:<30}")
