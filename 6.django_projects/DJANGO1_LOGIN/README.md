# 기초 개발 환경 셋업

## 패키지 설치 (현재 버전기준 3.2.10 설치됨)
pip install django==3.2

## 프로젝트 생성 (디렉토리는 무조건 생성됨)
django-admin startproject myproj

## 기본 프로젝트 환경 셋업
cd myproj
pip install django-dotenv

## DB 초기 셋업
python manage.py migrate

## 서버 구동
python manage.py runserver

http://localhost:8000


# 계정생성

## 관리자 계정 생성
python manage.py createsuperuser

http://localhost:8000/admin

## 기본 settings.py 설정 변경
언어 변경 (한국어로)
LANGUAGE_CODE = 'ko-kr'

로그인 안 된 상태로 페이지 접속 시 자동으로 리디렉션할 경로
LOGIN_URL = '/login/'

관리자 페이지 접근제어
ALLOWED_HOSTS = [
    '192.168.0.0/24',
    '127.0.0.1',
]

