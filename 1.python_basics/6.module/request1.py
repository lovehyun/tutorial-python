# 외부 라이브러리 설치 필요
# pip install requests
import requests

# 1. 웹 페이지 내용 가져오기
response = requests.get("https://www.example.com")
print("웹 페이지 내용:")
print(response.text)


# 2. GET 요청으로 JSON 데이터 가져오기
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
data = response.json()  # JSON 데이터를 파싱합니다.
print("JSON 데이터:")
print(data)


# 3. POST 요청 보내기
url = "https://httpbin.org/post"
payload = {"name": "John", "age": 30}
response = requests.post(url, json=payload)
print("POST 응답 데이터:")
print(response.json())


# 4. 헤더와 함께 요청 보내기
url = "https://www.example.com"
headers = {
    "User-Agent": "my-app/0.0.1",
    "Authorization": "Bearer your_token_here"
}
response = requests.get(url, headers=headers)
print("응답 상태 코드:", response.status_code)


# 5. 파일 다운로드
url = "https://www.example.com/somefile.zip"
response = requests.get(url)
filename = "downloaded_file.zip"

with open(filename, "wb") as file:
    file.write(response.content)

print(f"파일이 {filename}으로 저장되었습니다.")


# 6. 타임아웃 설정
try:
    response = requests.get("https://www.example.com", timeout=5)
    print("응답 상태 코드:", response.status_code)
except requests.Timeout:
    print("요청이 타임아웃되었습니다.")


# 7. 인증
from requests.auth import HTTPBasicAuth

url = "https://www.example.com/protected"
response = requests.get(url, auth=HTTPBasicAuth("username", "password"))
print("응답 상태 코드:", response.status_code)
