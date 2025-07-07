# 설치: pip install fastapi uvicorn
# 실행: uvicorn main_app:app --reload
# 테스트: 
#   1. 루트 경로 테스트:
#      curl -X GET "http://127.0.0.1:8000/"
#   2. 경로 매개변수 테스트:
#      curl -X GET "http://127.0.0.1:8000/items/1"
#   3. 경로 매개변수 및 쿼리 매개변수 테스트:
#      curl -X GET "http://127.0.0.1:8000/items/1?q=searchterm"
#   4. 사용자와 아이템 경로 매개변수 및 쿼리 매개변수 테스트:
#      curl -X GET "http://127.0.0.1:8000/users/1/items/2?item-query=something&short=true"
#   5. POST 요청 테스트:
#      curl -X POST "http://127.0.0.1:8000/items/" -H "Content-Type: application/json" -d '{"name": "ItemName", "description": "This is an item", "price": 10.5, "tax": 1.5}'

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Pydantic 모델 정의
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 루트 경로
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI example!"}

# 경로 매개변수
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = Query(None, max_length=50)):
    return {"item_id": item_id, "q": q}

# 쿼리 매개변수
@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id: int, 
    item_id: str, 
    q: Optional[str] = Query(None, alias="item-query"), 
    short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if short:
        item.update({"description": "This is a short item."})
    return item

# POST 요청 처리
@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
