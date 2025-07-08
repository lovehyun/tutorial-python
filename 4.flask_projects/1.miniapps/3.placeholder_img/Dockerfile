# 베이스 이미지 (Python 3.10 이상 추천)
# FROM python:3.10-slim
FROM python:3.9-slim-bullseye

# 작업 디렉토리 생성
WORKDIR /app

# 시스템 폰트 설치 (Noto + DejaVu)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        fonts-noto \
        fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

# 필요한 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5000 포트 개방 (Flask 기본 포트)
EXPOSE 5000

# Flask 앱 실행
# CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app3_docker:app"]

# nginx 프록시 헤더 설정
# location /placeholder/ {
#     proxy_pass http://flask:5000/;
#     proxy_set_header X-Forwarded-Prefix /placeholder;
# }
