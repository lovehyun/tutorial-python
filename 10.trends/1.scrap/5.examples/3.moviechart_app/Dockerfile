FROM python:3.10-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 생성
WORKDIR /app

# 파일 복사
COPY . /app

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 5000

# 서버 실행
CMD ["python", "3.moviechart3_show_highlight.py"]
