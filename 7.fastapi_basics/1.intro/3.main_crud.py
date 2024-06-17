# 설치: pip install fastapi uvicorn
# 실행: uvicorn main_crud:app --reload
# 테스트: 
#   1. 루트 경로 테스트:
#      curl -X GET "http://127.0.0.1:8000/"
#   2. 특정 아이템 조회 (GET 요청):
#      curl -X GET "http://127.0.0.1:8000/items/1"
#   3. 아이템 생성 (POST 요청):
#      curl -X POST "http://127.0.0.1:8000/items/" -H "Content-Type: application/json" -d '{"name": "ItemName", "description": "This is an item", "price": 10.5, "tax": 1.5}'
#   4. 아이템 업데이트 (PUT 요청):
#      curl -X PUT "http://127.0.0.1:8000/items/1" -H "Content-Type: application/json" -d '{"name": "UpdatedItemName", "description": "This is an updated item", "price": 12.5, "tax": 2.0}'
#   5. 아이템 삭제 (DELETE 요청):
#      curl -X DELETE "http://127.0.0.1:8000/items/1"

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Pydantic 모델을 사용하여 데이터 검증
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 메모리 데이터베이스 역할을 할 딕셔너리
fake_db = {}

# GET 요청
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return fake_db.get(item_id, {"Error": "Item not found"})

# POST 요청
@app.post("/items/")
def create_item(item: Item):
    item_id = len(fake_db) + 1
    fake_db[item_id] = item.model_dump()
    return {"item_id": item_id, **item.model_dump()}

# PUT 요청
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id in fake_db:
        fake_db[item_id] = item.model_dump()
        return {"message": "Item updated successfully", "item_id": item_id, **item.model_dump()}
    return {"Error": "Item not found"}

# DELETE 요청
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in fake_db:
        del fake_db[item_id]
        return {"message": "Item deleted successfully"}
    return {"Error": "Item not found"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
