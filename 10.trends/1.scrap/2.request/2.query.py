import requests

# 1. 헤더 추가하기
url = 'https://example.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)


# 2. POST 요청 보내기
url = 'https://example.com/login'
data = {
    'username': 'myusername',
    'password': 'mypassword'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)


# 3. 쿼리 파라미터 추가하기
url = 'https://example.com/login'
data = {
    'username': 'myusername',
    'password': 'mypassword'
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)


# 4. JSON 데이터 요청 및 파싱
url = 'https://api.example.com/data'
response = requests.get(url)

# JSON 데이터를 파싱합니다.
data = response.json()

# JSON 데이터 출력
print(data)


# 파일 다운로드
url = 'https://example.com/somefile.zip'
response = requests.get(url)

# 바이너리 파일로 저장
with open('somefile.zip', 'wb') as f:
    f.write(response.content)
