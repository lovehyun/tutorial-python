# 설치: pip install fastapi uvicorn
# 실행: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
