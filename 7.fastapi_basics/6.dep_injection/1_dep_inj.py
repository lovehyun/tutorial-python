# 6-1. 의존성 함수 정의
def common_query(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# 6-1. 의존성 주입하기
from fastapi import Depends, FastAPI

app = FastAPI()

@app.get("/items/")
def read_items(commons: dict = Depends(common_query)):
    return commons


# 6-2. 여러 라우트에서 재사용
@app.get("/products/")
def read_products(commons: dict = Depends(common_query)):
    return commons


# 6-3. 인증 처리 예제 (의존성 활용)
from fastapi import HTTPException, Header

# 6-3-1. 간단한 토큰 검증 함수
def verify_token(token: str = Header(...)):
    if token != "secrettoken":
        raise HTTPException(status_code=401, detail="Invalid Token")
    return token

# 6-3-2. 라우트에 적용
@app.get("/secure-data/")
def get_secure_data(token: str = Depends(verify_token)):
    return {"message": "You are authorized!"}


# 6-4. 클래스 기반 의존성 주입
class CommonParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/class-items/")
def read_items(params: CommonParams = Depends()):
    return {"skip": params.skip, "limit": params.limit}
