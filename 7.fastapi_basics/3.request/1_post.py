from fastapi import FastAPI

app = FastAPI()

# 3-1. POST 요청 기본
@app.post("/items")
def create_item(item: dict):
    return {"received_item": item}


# 3-2. Pydantic 모델 사용 (권장)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 요청 데이터 스키마 정의
class Item(BaseModel):
    name: str
    price: float
    description: str = None  # 선택 사항

@app.post("/items")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}


# 3-3. 요청 Body + Query 파라미터 함께 사용
@app.post("/orders")
def create_order(item: Item, quantity: int = 1):
    return {
        "item": item.name,
        "quantity": quantity,
        "total_price": item.price * quantity
    }


# 3-4. Form 데이터 받기 (예: HTML 폼 전송 시)
# username=testuser&password=1234
from fastapi import Form

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}


# 3-5. 파일 업로드 처리
from fastapi import File, UploadFile

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
