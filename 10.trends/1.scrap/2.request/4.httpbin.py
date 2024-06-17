import requests

def test_httpbin():
    base_url = "https://httpbin.org"

    # GET 요청 테스트
    def test_get():
        url = f"{base_url}/get"
        params = {'key': 'value'}
        response = requests.get(url, params=params)
        print("GET 요청 테스트:")
        print(response.json())
        print("\n")

    # POST 요청 테스트
    def test_post():
        url = f"{base_url}/post"
        data = {'key': 'value'}
        response = requests.post(url, data=data)
        print("POST 요청 테스트:")
        print(response.json())
        print("\n")

    # PUT 요청 테스트
    def test_put():
        url = f"{base_url}/put"
        data = {'key': 'value'}
        response = requests.put(url, data=data)
        print("PUT 요청 테스트:")
        print(response.json())
        print("\n")

    # DELETE 요청 테스트
    def test_delete():
        url = f"{base_url}/delete"
        response = requests.delete(url)
        print("DELETE 요청 테스트:")
        print(response.json())
        print("\n")

    # PATCH 요청 테스트
    def test_patch():
        url = f"{base_url}/patch"
        data = {'key': 'value'}
        response = requests.patch(url, data=data)
        print("PATCH 요청 테스트:")
        print(response.json())
        print("\n")

    # Headers 테스트
    def test_headers():
        url = f"{base_url}/headers"
        headers = {'User-Agent': 'my-app/0.0.1'}
        response = requests.get(url, headers=headers)
        print("Headers 테스트:")
        print(response.json())
        print("\n")

    # Status 코드 테스트
    def test_status_code():
        url = f"{base_url}/status/404"
        response = requests.get(url)
        print("Status 코드 테스트 (404):")
        print(response.status_code)
        print("\n")

    # Gzip 압축 테스트
    def test_gzip():
        url = f"{base_url}/gzip"
        response = requests.get(url)
        print("Gzip 압축 테스트:")
        print(response.json())
        print("\n")

    # IP 주소 테스트
    def test_ip():
        url = f"{base_url}/ip"
        response = requests.get(url)
        print("IP 주소 테스트:")
        print(response.json())
        print("\n")

    # User-Agent 테스트
    def test_user_agent():
        url = f"{base_url}/user-agent"
        response = requests.get(url)
        print("User-Agent 테스트:")
        print(response.json())
        print("\n")

    # 호출할 테스트 함수 목록
    tests = [test_get, test_post, test_put, test_delete, test_patch, test_headers, test_status_code, test_gzip, test_ip, test_user_agent]

    # 각 테스트 실행
    for test in tests:
        test()

# 테스트 함수 실행
test_httpbin()
