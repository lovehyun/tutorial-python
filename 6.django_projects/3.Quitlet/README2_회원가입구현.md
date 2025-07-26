# 회원가입/로그인 시스템 구현

## 1. accounts/forms.py 생성

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap 클래스 적용
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap 클래스 적용
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
```

## 2. accounts/views.py

```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}님, 회원가입이 완료되었습니다!')
            # 회원가입 후 자동 로그인
            login(request, user)
            return redirect('quiz:home')
        else:
            messages.error(request, '회원가입 정보를 다시 확인해주세요.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('quiz:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{username}님, 환영합니다!')
                # next 파라미터가 있으면 해당 페이지로, 없으면 홈으로
                next_page = request.GET.get('next', 'quiz:home')
                return redirect(next_page)
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, '로그아웃되었습니다.')
    return redirect('quiz:home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
```

## 3. templates 폴더 구조 생성

```bash
# 프로젝트 루트에 templates 폴더 생성
mkdir templates
mkdir templates\base
mkdir templates\accounts
mkdir templates\quiz
```

## 4. templates/base/base.html

```html
<!-- templates/base/base.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Quizlet 클론{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- 네비게이션 바 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'quiz:home' %}">
                <strong>Quizlet 클론</strong>
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'quiz:home' %}">홈</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'quiz:question_list' %}">문제 목록</a>
                    </li>
                </ul>
                
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                                {{ user.username }}님
                            </a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="{% url 'accounts:profile' %}">프로필</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item" href="{% url 'accounts:logout' %}">로그아웃</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:login' %}">로그인</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:signup' %}">회원가입</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- 메시지 표시 -->
    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- 메인 콘텐츠 -->
    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center py-3 mt-5">
        <div class="container">
            <p>&copy; 2025 Quizlet 클론. Made with Django</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## 5. templates/accounts/signup.html

```html
<!-- templates/accounts/signup.html -->
{% extends 'base/base.html' %}

{% block title %}회원가입 - Quizlet 클론{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3 class="text-center">회원가입</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    {% for field in form %}
                        <div class="mb-3">
                            <label for="{{ field.id_for_label }}" class="form-label">
                                {{ field.label }}
                            </label>
                            {{ field }}
                            {% if field.help_text %}
                                <div class="form-text">{{ field.help_text }}</div>
                            {% endif %}
                            {% if field.errors %}
                                {% for error in field.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            {% endif %}
                        </div>
                    {% endfor %}
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">회원가입</button>
                    </div>
                </form>
                
                <div class="text-center mt-3">
                    <p>이미 계정이 있으신가요? <a href="{% url 'accounts:login' %}">로그인</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 6. templates/accounts/login.html

```html
<!-- templates/accounts/login.html -->
{% extends 'base/base.html' %}

{% block title %}로그인 - Quizlet 클론{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3 class="text-center">로그인</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    {% for field in form %}
                        <div class="mb-3">
                            <label for="{{ field.id_for_label }}" class="form-label">
                                {{ field.label }}
                            </label>
                            {{ field }}
                            {% if field.errors %}
                                {% for error in field.errors %}
                                    <div class="text-danger">{{ error }}</div>
                                {% endfor %}
                            {% endif %}
                        </div>
                    {% endfor %}
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">로그인</button>
                    </div>
                </form>
                
                <div class="text-center mt-3">
                    <p>계정이 없으신가요? <a href="{% url 'accounts:signup' %}">회원가입</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 7. templates/accounts/profile.html

```html
<!-- templates/accounts/profile.html -->
{% extends 'base/base.html' %}

{% block title %}프로필 - Quizlet 클론{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h3>프로필 정보</h3>
            </div>
            <div class="card-body">
                <table class="table">
                    <tr>
                        <th>사용자명:</th>
                        <td>{{ user.username }}</td>
                    </tr>
                    <tr>
                        <th>이메일:</th>
                        <td>{{ user.email }}</td>
                    </tr>
                    <tr>
                        <th>이름:</th>
                        <td>{{ user.first_name }} {{ user.last_name }}</td>
                    </tr>
                    <tr>
                        <th>가입일:</th>
                        <td>{{ user.date_joined|date:"Y년 m월 d일" }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5>학습 통계</h5>
            </div>
            <div class="card-body">
                <p>구현 예정...</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 8. accounts/urls.py 수정

```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
```

## 9. settings.py에 TEMPLATES 설정 수정

```python
# settings.py
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 이 줄 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 로그인 성공 후 리다이렉트할 URL
LOGIN_REDIRECT_URL = '/'
# 로그아웃 후 리다이렉트할 URL  
LOGOUT_REDIRECT_URL = '/'
# 로그인이 필요한 페이지 접근 시 리다이렉트할 URL
LOGIN_URL = '/accounts/login/'
```

## 10. static/css/style.css 생성

```css
/* static/css/style.css */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: none;
}

.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}

footer {
    margin-top: auto;
}

.alert {
    margin-bottom: 0;
}
```

이제 회원가입/로그인 시스템이 완성되었습니다! 다음 단계는 quiz 앱의 홈페이지와 문제 목록 뷰를 만들어야 합니다.

## 11. 다음 TODO 참고

### 1. quiz 앱의 기본 뷰들 만들기
- 홈페이지 (quiz:home)
- 문제 목록 (quiz:question_list)

### 2. 관리자 페이지에서 테스트 데이터 추가
- 카테고리, 문제집, 문제들 몇 개 만들기

### 3. 퀴즈 모드 구현
- 시험 보기 기능

## 지금 당장 해야 할 일

위 코드들을 각 파일에 복사해서 넣으시고, 개발 서버를 실행해보세요:

```bash
python manage.py runserver
```

그러면 http://127.0.0.1:8000/accounts/signup/에서 회원가입을 테스트할 수 있습니다.

하지만 아직 quiz:home URL이 없어서 에러가 날 수 있으니, quiz 앱의 기본 뷰들을 먼저 만들까요? 아니면 관리자 페이지에서 문제 데이터부터 추가해볼까요?
