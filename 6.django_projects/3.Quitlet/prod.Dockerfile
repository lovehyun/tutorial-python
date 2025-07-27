FROM python:3.10-slim

# 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 필수 라이브러리 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && \
    pip install gunicorn

COPY . .

RUN mkdir -p /app/media /app/static

# collectstatic (정적 파일 수집 자동화)
RUN python manage.py collectstatic --noinput

# 운영용 서버 실행
CMD ["gunicorn", "quizproject.wsgi:application", "--bind", "0.0.0.0:8000"]
