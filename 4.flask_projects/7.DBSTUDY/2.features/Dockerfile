# 공식 Python 런타임을 부모 이미지로 사용
FROM python:3.8-slim

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리에 복사
COPY . /app

# requirements.txt에 명시된 필요한 패키지를 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 5000번을 외부에 공개
EXPOSE 5000

# 환경 변수 설정
ENV FLASK_APP=app.py

# 컨테이너가 시작될 때 flask run 명령을 실행
CMD ["flask", "run", "--host=0.0.0.0"]
