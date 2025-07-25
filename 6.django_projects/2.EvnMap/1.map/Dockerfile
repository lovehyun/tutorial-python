# 베이스 이미지 설정
FROM python:3.8

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 소스 코드 복사
COPY . .

# 컨테이너 실행 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]
