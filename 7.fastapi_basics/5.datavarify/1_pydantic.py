from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import BaseModel, Field

app = FastAPI()

# 5-1. Pydantic 기본 모델 작성
# class User(BaseModel):
#     username: str
#     age: int
#     email: str

# 5-2. 필드 기본값 및 선택 필드
# 5-3. 필드에 유효성 조건 추가
class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., gt=0, lt=150)  # 0세 초과, 150세 미만
    email: str = None  # 선택 사항
    is_active: bool = True  # 기본값 True

@app.post("/users")
def create_user(user: User):
    return {"username": user.username, "age": user.age, "email": user.email}


# 5-4. Path Parameter 유효성 검사
from fastapi import Path

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., gt=0)):
    return {"item_id": item_id}


# 5-5. Query Parameter 유효성 검사
from fastapi import Query

@app.get("/search")
def search_items(keyword: str = Query(..., min_length=2), page: int = Query(1, ge=1)):
    return {"keyword": keyword, "page": page}


# 5-6. 응답 모델 사용 (Response Model)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    age: int

@app.get("/user", response_model=User)
def get_user():
    return {"username": "Alice", "age": 30, "extra_field": "ignore me"}
