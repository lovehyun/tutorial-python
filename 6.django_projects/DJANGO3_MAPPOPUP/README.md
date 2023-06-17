# 기초 개발 환경 셋업

## 패키지 설치 (현재 버전기준 3.2.10 설치됨)
pip install django==3.2
pip install elasticsearch==7.15
pip install python-dotenv

## 프로젝트 생성 (디렉토리는 무조건 생성됨)
django-admin startproject evnsol

## 프로젝트 내 애플리케이션 생성
python manage.py startapp myapp

## 기본 프로젝트 환경 셋업
cd evnsol
pip install django-dotenv

## DB 초기 셋업
python manage.py migrate

## 서버 구동
python manage.py runserver

http://localhost:8000

또는

python manage.py runserver 0.0.0.0:8888
(기본값은 127.0.0.1:8000)


# 계정생성

## 관리자 계정 생성
python manage.py createsuperuser

http://localhost:8000/admin

## 기본 settings.py 설정 변경
언어 변경 (한국어로)
LANGUAGE_CODE = 'ko-kr'

로그인 안 된 상태로 페이지 접속 시 자동으로 리디렉션할 경로
LOGIN_URL = '/login/'

관리자 페이지 접근제어 (DEBUG=True 일때의 기본값은 localhost, 127.0.0.1)
ALLOWED_HOSTS = [
    '192.168.0.0/24',
    '127.0.0.1',
]


# 배포준비

## settings.py 마무리
DEBUG = False

STATIC_URL = '/static'
STATIC_ROOT = BASE_DIR / 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

python manage.py collectstatic

또는

python manage.py runserver --insecure


## 각종 민감정보 및 파일 관리

secret_key.txt 별도 생성 및 settings.py 에서 제거

with open(os.path.join(BASE_DIR, 'www', 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()


db.sqlite3 별도 관리

DATABASES = {
    'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
}


## 웹 서버와 연동

apache 또는 nginx 등과 연동

### apache 와 연동
apt install httpd
pip install mod_wsgi

mod_wsgi-express start-server myproj/wsgi.py

### nginx 와 연동
apt install nginx

nginx.conf
location /static/ {
    root /www/static/;
}
location / {
    include /www/uwsgi_params;
    uwsgi_pass 127.0.0.1:8000;
}


