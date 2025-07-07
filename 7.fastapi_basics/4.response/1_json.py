from fastapi import FastAPI

app = FastAPI()

# 4-1. 기본 JSON 응답
@app.get("/hello")
def hello():
    return {"message": "Hello, FastAPI!"}


# 4-2. 응답 상태 코드 변경
from fastapi import status

@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_item():
    return {"message": "Item created successfully!"}


# 4-3. 커스텀 Response 객체 사용
from fastapi.responses import JSONResponse

@app.get("/custom")
def custom_response():
    return JSONResponse(content={"message": "Custom response"}, status_code=202)


# 4-4. HTML 응답
from fastapi.responses import HTMLResponse

@app.get("/html", response_class=HTMLResponse)
def get_html():
    return """
    <html>
        <head><title>FastAPI HTML</title></head>
        <body><h1>Hello FastAPI!</h1></body>
    </html>
    """

# 4-5. 파일 응답
from fastapi.responses import FileResponse

@app.get("/download")
def download_file():
    return FileResponse("sample.pdf", media_type='application/pdf', filename="download.pdf")


# 4-6. Redirect 응답
from fastapi.responses import RedirectResponse

@app.get("/move")
def redirect_example():
    return RedirectResponse(url="/hello")
