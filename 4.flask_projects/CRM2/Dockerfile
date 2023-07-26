# 베이스 이미지 설정
FROM python:3.8-slim-buster

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# 애플리케이션 파일 복사
COPY . .

# Flask 애플리케이션 실행 명령어
# CMD ["python", "app.py"]
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "-w", "4"]
