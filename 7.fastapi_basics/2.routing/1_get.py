from fastapi import FastAPI

app = FastAPI()

# 2-1. 기본 GET 요청 처리
@app.get("/")
def home():
    return {"message": "This is the Home Page"}

# 2-2. Path Parameter (경로 변수)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# 2-3. Query Parameter (쿼리 문자열)
@app.get("/search")
def search_item(keyword: str = "default"):
    return {"keyword": keyword}

# 2-4. Path + Query 혼합 사용
@app.get("/users/{user_id}/items")
def get_user_item(user_id: int, item: str = "default"):
    return {"user_id": user_id, "item": item}
