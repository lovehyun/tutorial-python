import requests

# GET 요청 보내기
response = requests.get("https://api.github.com/")

# 응답 상태 코드 확인
if response.status_code == 200:
    print("요청이 성공했습니다.")
else:
    print("요청이 실패했습니다.")

# 응답 텍스트 출력
print("응답 내용:")
print(response.text)
