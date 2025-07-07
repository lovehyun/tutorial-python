from fastapi import FastAPI, HTTPException

app = FastAPI()

# 8-1. 기본 예외 처리 (HTTPException 사용)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive.")
    return {"item_id": item_id}


# 8-2. 커스텀 예외 클래스 만들기
class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

# 8-2. 커스텀 예외 핸들러 추가
from fastapi.responses import JSONResponse
from fastapi.requests import Request

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.get("/custom-error/{name}")
def raise_custom(name: str):
    if name == "error":
        raise CustomException(name=name)
    return {"name": name}


# 8-3. 전역 에러 처리 (기본 예외 핸들러)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )


# 8-4. ValidationError 처리 (요청 검증 실패 시)
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Custom validation error.", "details": exc.errors()}
    )
