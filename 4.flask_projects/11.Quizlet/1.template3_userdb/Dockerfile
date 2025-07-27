# 베이스 이미지: Python 3.10
FROM python:3.10-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 작업 디렉토리 생성
WORKDIR /app

# 필요한 패키지 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . /app/

# 필요한 디렉토리 생성
RUN mkdir -p data/uploads

# 포트 노출
EXPOSE 5000

# Production용 실행 (Gunicorn 사용)
CMD ["sh", "-c", "python database.py && gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 60 app:app"]
