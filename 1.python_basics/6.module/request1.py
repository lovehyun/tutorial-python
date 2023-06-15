# 외부 라이브러리 설치 필요
# pip install requests
import requests

# 웹 페이지 내용 가져오기
response = requests.get("https://www.example.com")
print("웹 페이지 내용:")
print(response.text)

