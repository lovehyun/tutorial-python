from fastapi import FastAPI, Request
import time

app = FastAPI()

# 7-1. 미들웨어 기본 구조
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # 요청 처리
    response = await call_next(request)

    # 처리 시간 측정
    process_time = time.time() - start_time
    print(f"Request: {request.url} took {process_time:.4f} seconds")

    return response


# 7-2. 요청 헤더 검사 (간단 인증 미들웨어)
from fastapi.responses import JSONResponse

@app.middleware("http")
async def check_token(request: Request, call_next):
    token = request.headers.get('token')
    if token != "secrettoken":
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    
    response = await call_next(request)
    return response


# 7-3. 처리 시간 응답에 추가하기
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# 7-4. CORS 미들웨어 설정
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
