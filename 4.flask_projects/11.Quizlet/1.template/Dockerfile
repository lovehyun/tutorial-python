# 베이스 이미지: Python 3.10
FROM python:3.10-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성
WORKDIR /app

# 필요한 패키지 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 전체 앱 코드 복사
COPY . /app/

# 업로드 디렉토리 미리 생성
RUN mkdir -p uploads

# Flask 실행
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
