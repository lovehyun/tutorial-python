FROM python:3.9-slim-bullseye

WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 5000 노출
EXPOSE 5000

# 환경 변수 설정 (옵션)
ENV APPLICATION_ROOT="/catchmind"

# 애플리케이션 실행
CMD ["python", "server.py"]
