# 설치: pip install fastapi uvicorn
# 실행: uvicorn myapp:app --reload

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
