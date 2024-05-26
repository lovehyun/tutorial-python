import requests

# 요청을 보낼 웹 페이지의 URL
url = 'https://www.example.com'

# GET 요청 보내기
response = requests.get(url)

# 응답 확인
if response.status_code == 200:
    # HTML 내용 출력
    print(response.text)
else:
    print("요청에 실패하였습니다. 상태 코드:", response.status_code)
