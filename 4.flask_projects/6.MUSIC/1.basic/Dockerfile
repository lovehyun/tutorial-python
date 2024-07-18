# 베이스 이미지로 Python 3.9 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지들을 복사
COPY requirements.txt requirements.txt

# 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Flask 환경변수 설정
ENV FLASK_APP=app_sqlalchemy.py
ENV FLASK_ENV=development

# 데이터베이스 초기화 스크립트 실행 (필요한 경우)
# RUN flask db init && flask db migrate && flask db upgrade

# 컨테이너 포트 설정
EXPOSE 5000

# 애플리케이션 실행 명령
CMD ["flask", "run", "--host=0.0.0.0"]
