# Django Quizlet 프로젝트 셋업 가이드

## 1. 개발 환경 준비

### 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```

### 필수 패키지 설치
```bash
# Django 및 기본 패키지 설치
pip install django
pip install pillow  # 이미지 처리용 (프로필 이미지 등)

# requirements.txt 생성
pip freeze > requirements.txt
```

## 2. Django 프로젝트 생성

```bash
# 프로젝트 생성
django-admin startproject quizlet_clone .

# 앱 생성
python manage.py startapp accounts    # 회원관리
python manage.py startapp quiz        # 퀴즈 관련
```

## 3. 프로젝트 구조

```
quizlet_clone/
├── manage.py
├── requirements.txt
├── quizlet_clone/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── quiz/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
```

## 4. settings.py 기본 설정

```python
# quizlet_clone/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  # 추가
    'quiz',      # 추가
]

# 한국어/시간대 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

# 미디어 파일 설정 (이미지 업로드용)
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 정적 파일 설정
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

### 기본 폴더 생성
```bash
# 프로젝트 루트에서 실행
mkdir static
mkdir static\css
mkdir static\js
mkdir static\images
```

## 5. 기본 URL 설정

### 메인 urls.py
```python
# quizlet_clone/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### accounts/urls.py 생성
```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

### quiz/urls.py 생성
```python
# quiz/urls.py
from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.question_list, name='question_list'),
    path('quiz/<int:quiz_id>/', views.quiz_mode, name='quiz_mode'),
]
```

## 6. 데이터베이스 초기 설정

```bash
# 마이그레이션 생성 및 적용
python manage.py makemigrations
python manage.py migrate

# 관리자 계정 생성
python manage.py createsuperuser
```

## 7. 정적 파일 폴더 생성

```bash
# 프로젝트 루트에 static 폴더 생성
mkdir static
mkdir static/css
mkdir static/js
mkdir static/images

# templates 폴더 생성
mkdir templates
```

## 8. 개발 서버 실행

```bash
# 개발 서버 시작
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000`으로 접속하면 Django 기본 페이지가 보입니다.

## 9. 다음 단계

이제 기본 셋업이 완료되었습니다. 다음으로 진행할 작업들:

1. **모델 설계** - User, Question, Quiz, Result 모델 생성
2. **회원가입/로그인** - 기본 인증 시스템 구현
3. **문제 관리** - CRUD 기능 구현
4. **퀴즈 모드** - 시험 기능 구현
5. **프론트엔드** - HTML, CSS, JavaScript로 UI 구성

각 단계별로 구체적인 코드가 필요하시면 말씀해 주세요!
