# pip install websockets

import asyncio
import websockets

# 클라이언트 연결 시 실행되는 함수
async def handle_client(websocket):
    print("클라이언트 연결됨!")

    # 연결 직후 메시지 전송
    await websocket.send("서버에 연결되었습니다!")

    try:
        async for message in websocket:
            print("클라이언트 메시지:", message)

            # 받은 메시지를 다시 클라이언트에 돌려보냄
            await websocket.send(f"서버가 받은 메시지: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("클라이언트 연결 종료")


async def main():
    # WebSocket 서버 실행
    async with websockets.serve(handle_client, "localhost", 8080):
        print("WebSocket 서버 실행 중 (ws://localhost:8080)")
        await asyncio.Future()  # 서버 계속 실행


# 프로그램 시작
asyncio.run(main())
