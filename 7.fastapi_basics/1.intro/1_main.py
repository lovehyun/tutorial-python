# 설치: pip install fastapi uvicorn
# 실행: uvicorn main:app --reload

# FastAPI는 프레임워크입니다.
# FastAPI는 웹 서버가 아닙니다.
# FastAPI는 API 애플리케이션을 만드는 도구이고, 실제로 HTTP 요청을 받아서 처리해주는 서버가 따로 필요합니다.

# uvicorn은 FastAPI의 ASGI 서버입니다.
# uvicorn은 **ASGI (Asynchronous Server Gateway Interface)**를 지원하는 웹 서버입니다.

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# Swagger: http://127.0.0.1:8000/docs
# Redoc: http://127.0.0.1:8000/redoc
