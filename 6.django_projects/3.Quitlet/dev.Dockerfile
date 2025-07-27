FROM python:3.10-slim

# 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리
WORKDIR /app

# pip 업그레이드 + 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 프로젝트 전체 복사
COPY . .

# 미디어 폴더 생성 (선택)
RUN mkdir -p /app/media

# 서버 실행 (Django 개발용)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
