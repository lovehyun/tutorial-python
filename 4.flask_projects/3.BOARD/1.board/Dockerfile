FROM python:3.9-slim-bullseye

WORKDIR /app

# SQLite3 설치
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 데이터베이스 초기화
RUN sqlite3 board.db < init_database.sql

# 포트 5000 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "app_fetch.py"]
