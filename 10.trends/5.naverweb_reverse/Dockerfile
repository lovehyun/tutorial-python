FROM python:3.10-slim-bullseye

WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 5000 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "5.naver_lyric_be.py"]
