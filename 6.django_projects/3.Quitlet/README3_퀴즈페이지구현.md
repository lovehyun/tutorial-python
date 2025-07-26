# 퀴즈 페이지 시스템 구현

## 1. quiz/views.py

```python
# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
import json

from .models import QuestionSet, Question, Choice, Quiz, QuizResult, Category, StudyProgress

def home_view(request):
    """홈페이지"""
    # 최신 문제집들
    latest_sets = QuestionSet.objects.filter(is_public=True).order_by('-created_at')[:6]
    
    # 카테고리별 문제집 수
    categories = Category.objects.annotate(
        question_set_count=Count('questionset')
    ).filter(question_set_count__gt=0)
    
    # 사용자가 로그인한 경우 최근 학습 기록
    recent_progress = None
    if request.user.is_authenticated:
        recent_progress = StudyProgress.objects.filter(
            user=request.user
        ).select_related('question_set').order_by('-last_studied')[:3]
    
    context = {
        'latest_sets': latest_sets,
        'categories': categories,
        'recent_progress': recent_progress,
    }
    return render(request, 'quiz/home.html', context)

def question_set_list(request):
    """문제집 목록"""
    category_id = request.GET.get('category')
    search = request.GET.get('search')
    
    question_sets = QuestionSet.objects.filter(is_public=True).select_related('category', 'creator')
    
    if category_id:
        question_sets = question_sets.filter(category_id=category_id)
    
    if search:
        question_sets = question_sets.filter(title__icontains=search)
    
    question_sets = question_sets.annotate(
        question_count=Count('questions')
    ).order_by('-created_at')
    
    categories = Category.objects.all()
    
    context = {
        'question_sets': question_sets,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search,
    }
    return render(request, 'quiz/question_set_list.html', context)

def question_set_detail(request, pk):
    """문제집 상세보기 (4지선다 전체 문제와 답안)"""
    question_set = get_object_or_404(QuestionSet, pk=pk, is_public=True)
    questions = question_set.questions.prefetch_related('choices').order_by('order', 'created_at')
    
    # 사용자의 학습 기록
    user_progress = None
    if request.user.is_authenticated:
        user_progress, created = StudyProgress.objects.get_or_create(
            user=request.user,
            question_set=question_set
        )
        if not created:
            user_progress.times_studied += 1
            user_progress.save()
    
    context = {
        'question_set': question_set,
        'questions': questions,
        'user_progress': user_progress,
    }
    return render(request, 'quiz/question_set_detail.html', context)

@login_required
def quiz_start(request, pk):
    """퀴즈 시작"""
    question_set = get_object_or_404(QuestionSet, pk=pk, is_public=True)
    
    if request.method == 'POST':
        # 새 퀴즈 세션 생성
        quiz = Quiz.objects.create(
            question_set=question_set,
            user=request.user,
            title=f"{question_set.title} - 퀴즈",
            total_questions=question_set.questions.count()
        )
        return redirect('quiz:quiz_take', quiz_id=quiz.id)
    
    context = {
        'question_set': question_set,
        'question_count': question_set.questions.count(),
    }
    return render(request, 'quiz/quiz_start.html', context)

@login_required
def quiz_take(request, quiz_id):
    """퀴즈 응시"""
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user, is_completed=False)
    questions = quiz.question_set.questions.prefetch_related('choices').order_by('order', 'created_at')
    
    # 이미 답변한 문제들
    answered_questions = QuizResult.objects.filter(quiz=quiz).values_list('question_id', flat=True)
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'answered_questions': list(answered_questions),
        'total_questions': questions.count(),
        'answered_count': len(answered_questions),
    }
    return render(request, 'quiz/quiz_take.html', context)

@login_required
def quiz_submit_answer(request, quiz_id):
    """퀴즈 답안 제출 (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user, is_completed=False)
    
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        choice_id = data.get('choice_id')
        
        question = get_object_or_404(Question, id=question_id, question_set=quiz.question_set)
        choice = get_object_or_404(Choice, id=choice_id, question=question)
        
        # 기존 답안이 있다면 업데이트, 없다면 생성
        quiz_result, created = QuizResult.objects.get_or_create(
            quiz=quiz,
            question=question,
            defaults={
                'selected_choice': choice,
                'is_correct': choice.is_correct,
            }
        )
        
        if not created:
            quiz_result.selected_choice = choice
            quiz_result.is_correct = choice.is_correct
            quiz_result.save()
        
        # 정답 여부와 정답 선택지 반환
        correct_choice = question.choices.filter(is_correct=True).first()
        
        return JsonResponse({
            'success': True,
            'is_correct': choice.is_correct,
            'correct_choice_id': correct_choice.id if correct_choice else None,
            'explanation': question.explanation,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def quiz_complete(request, quiz_id):
    """퀴즈 완료"""
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    
    if not quiz.is_completed:
        # 점수 계산
        results = QuizResult.objects.filter(quiz=quiz)
        quiz.score = results.filter(is_correct=True).count()
        quiz.is_completed = True
        quiz.completed_at = timezone.now()
        quiz.time_taken = quiz.completed_at - quiz.started_at
        quiz.save()
        
        # 학습 진도 업데이트
        progress, created = StudyProgress.objects.get_or_create(
            user=request.user,
            question_set=quiz.question_set
        )
        if quiz.score > progress.best_score:
            progress.best_score = quiz.score
        progress.save()
    
    # 결과 분석
    results = QuizResult.objects.filter(quiz=quiz).select_related('question', 'selected_choice')
    correct_count = results.filter(is_correct=True).count()
    wrong_count = results.filter(is_correct=False).count()
    
    context = {
        'quiz': quiz,
        'results': results,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'percentage': quiz.get_percentage_score(),
    }
    return render(request, 'quiz/quiz_complete.html', context)

@login_required
def my_quizzes(request):
    """내 퀴즈 기록"""
    quizzes = Quiz.objects.filter(user=request.user).select_related('question_set').order_by('-started_at')
    
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quiz/my_quizzes.html', context)
```

## 2. quiz/urls.py 업데이트

```python
# quiz/urls.py
from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('sets/', views.question_set_list, name='question_list'),
    path('sets/<int:pk>/', views.question_set_detail, name='question_set_detail'),
    path('sets/<int:pk>/quiz/start/', views.quiz_start, name='quiz_start'),
    path('quiz/<int:quiz_id>/', views.quiz_take, name='quiz_take'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_submit_answer, name='quiz_submit_answer'),
    path('quiz/<int:quiz_id>/complete/', views.quiz_complete, name='quiz_complete'),
    path('my-quizzes/', views.my_quizzes, name='my_quizzes'),
]
```

## 3. templates/quiz/home.html

```html
<!-- templates/quiz/home.html -->
{% extends 'base/base.html' %}

{% block title %}홈 - Quizlet 클론{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="jumbotron bg-primary text-white p-5 rounded mb-4">
            <h1 class="display-4">Quizlet 클론에 오신 것을 환영합니다!</h1>
            <p class="lead">다양한 문제집으로 학습하고 퀴즈를 통해 실력을 테스트해보세요.</p>
            <a class="btn btn-light btn-lg" href="{% url 'quiz:question_list' %}">문제집 둘러보기</a>
        </div>
    </div>
</div>

{% if user.is_authenticated and recent_progress %}
<div class="row mb-4">
    <div class="col-12">
        <h3>최근 학습 기록</h3>
        <div class="row">
            {% for progress in recent_progress %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ progress.question_set.title }}</h5>
                        <p class="card-text">
                            <small class="text-muted">{{ progress.last_studied|date:"m월 d일" }}</small><br>
                            학습 횟수: {{ progress.times_studied }}회<br>
                            최고 점수: {{ progress.best_score }}점
                        </p>
                        <a href="{% url 'quiz:question_set_detail' progress.question_set.pk %}" class="btn btn-primary">다시 학습</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}

<div class="row mb-4">
    <div class="col-12">
        <h3>카테고리</h3>
        <div class="row">
            {% for category in categories %}
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">{{ category.name }}</h5>
                        <p class="card-text">{{ category.question_set_count }}개 문제집</p>
                        <a href="{% url 'quiz:question_list' %}?category={{ category.id }}" class="btn btn-outline-primary">보기</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <h3>최신 문제집</h3>
        <div class="row">
            {% for question_set in latest_sets %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ question_set.title }}</h5>
                        <p class="card-text">{{ question_set.description|truncatewords:15 }}</p>
                        <p class="card-text">
                            <small class="text-muted">
                                {{ question_set.creator.username }} · {{ question_set.created_at|date:"m월 d일" }}
                            </small>
                        </p>
                        <a href="{% url 'quiz:question_set_detail' question_set.pk %}" class="btn btn-primary">학습하기</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

## 4. templates/quiz/question_set_list.html

```html
<!-- templates/quiz/question_set_list.html -->
{% extends 'base/base.html' %}

{% block title %}문제집 목록 - Quizlet 클론{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>문제집 목록</h2>
</div>

<!-- 검색 및 필터 -->
<div class="row mb-4">
    <div class="col-md-8">
        <form method="get" class="d-flex">
            <input type="text" name="search" class="form-control me-2" placeholder="문제집 제목 검색..." value="{{ search_query }}">
            <button type="submit" class="btn btn-outline-primary">검색</button>
        </form>
    </div>
    <div class="col-md-4">
        <form method="get">
            <select name="category" class="form-select" onchange="this.form.submit()">
                <option value="">모든 카테고리</option>
                {% for category in categories %}
                <option value="{{ category.id }}" {% if category.id|stringformat:'s' == selected_category %}selected{% endif %}>
                    {{ category.name }}
                </option>
                {% endfor %}
            </select>
        </form>
    </div>
</div>

<!-- 문제집 목록 -->
<div class="row">
    {% for question_set in question_sets %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ question_set.title }}</h5>
                <p class="card-text">{{ question_set.description|truncatewords:20 }}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <span class="badge bg-primary">{{ question_set.question_count }}문제</span>
                        {% if question_set.category %}
                        <span class="badge bg-secondary">{{ question_set.category.name }}</span>
                        {% endif %}
                    </div>
                    <small class="text-muted">{{ question_set.creator.username }}</small>
                </div>
                <div class="mt-3">
                    <a href="{% url 'quiz:question_set_detail' question_set.pk %}" class="btn btn-primary">학습하기</a>
                    {% if user.is_authenticated %}
                    <a href="{% url 'quiz:quiz_start' question_set.pk %}" class="btn btn-success">퀴즈 시작</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12">
        <div class="alert alert-info text-center">
            <h4>문제집이 없습니다</h4>
            <p>검색 조건에 맞는 문제집을 찾을 수 없습니다.</p>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

## 5. templates/quiz/question_set_detail.html

```html
<!-- templates/quiz/question_set_detail.html -->
{% extends 'base/base.html' %}

{% block title %}{{ question_set.title }} - Quizlet 클론{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h3>{{ question_set.title }}</h3>
                {% if user.is_authenticated %}
                <a href="{% url 'quiz:quiz_start' question_set.pk %}" class="btn btn-success">
                    <i class="bi bi-play-fill"></i> 퀴즈 시작
                </a>
                {% endif %}
            </div>
            <div class="card-body">
                <p class="card-text">{{ question_set.description }}</p>
                <p class="text-muted">
                    <strong>작성자:</strong> {{ question_set.creator.username }} | 
                    <strong>문제 수:</strong> {{ questions.count }}개 |
                    <strong>작성일:</strong> {{ question_set.created_at|date:"Y년 m월 d일" }}
                </p>
            </div>
        </div>

        <!-- 문제 목록 -->
        <div class="mt-4">
            <h4>전체 문제와 정답</h4>
            {% for question in questions %}
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">문제 {{ forloop.counter }}</h5>
                    <p class="card-text">{{ question.question_text }}</p>
                    
                    {% if question.question_image %}
                    <img src="{{ question.question_image.url }}" class="img-fluid mb-3" alt="문제 이미지">
                    {% endif %}
                    
                    <div class="row">
                        {% for choice in question.choices.all %}
                        <div class="col-md-6 mb-2">
                            <div class="p-2 border rounded {% if choice.is_correct %}bg-success text-white{% else %}bg-light{% endif %}">
                                <strong>{{ forloop.counter }}.</strong> {{ choice.choice_text }}
                                {% if choice.is_correct %}
                                <span class="badge bg-warning text-dark ms-2">정답</span>
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    
                    {% if question.explanation %}
                    <div class="alert alert-info mt-3">
                        <strong>해설:</strong> {{ question.explanation }}
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <div class="col-md-4">
        {% if user.is_authenticated and user_progress %}
        <div class="card">
            <div class="card-header">
                <h5>나의 학습 기록</h5>
            </div>
            <div class="card-body">
                <p><strong>학습 횟수:</strong> {{ user_progress.times_studied }}회</p>
                <p><strong>최고 점수:</strong> {{ user_progress.best_score }}점</p>
                <p><strong>마지막 학습:</strong> {{ user_progress.last_studied|date:"m월 d일 H:i" }}</p>
            </div>
        </div>
        {% endif %}
        
        <div class="card mt-3">
            <div class="card-header">
                <h5>카테고리 정보</h5>
            </div>
            <div class="card-body">
                {% if question_set.category %}
                <p><strong>카테고리:</strong> {{ question_set.category.name }}</p>
                <p>{{ question_set.category.description }}</p>
                {% else %}
                <p>카테고리가 설정되지 않았습니다.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 6. templates/quiz/quiz_start.html

```html
<!-- templates/quiz/quiz_start.html -->
{% extends 'base/base.html' %}

{% block title %}퀴즈 시작 - {{ question_set.title }}{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header text-center">
                <h3>퀴즈 시작 준비</h3>
            </div>
            <div class="card-body text-center">
                <h4>{{ question_set.title }}</h4>
                <p class="lead">{{ question_set.description }}</p>
                
                <div class="alert alert-info">
                    <h5>퀴즈 정보</h5>
                    <p><strong>총 문제 수:</strong> {{ question_count }}문제</p>
                    <p><strong>출제 방식:</strong> 4지선다</p>
                    <p><strong>시간 제한:</strong> 없음</p>
                </div>
                
                <div class="alert alert-warning">
                    <h6>주의사항</h6>
                    <ul class="list-unstyled mb-0">
                        <li>• 한 번 선택한 답은 변경할 수 있습니다</li>
                        <li>• 모든 문제를 완료해야 결과를 볼 수 있습니다</li>
                        <li>• 브라우저를 새로고침하면 진행 상황이 사라집니다</li>
                    </ul>
                </div>
                
                <form method="post">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-success btn-lg">
                        <i class="bi bi-play-fill"></i> 퀴즈 시작하기
                    </button>
                </form>
                
                <div class="mt-3">
                    <a href="{% url 'quiz:question_set_detail' question_set.pk %}" class="btn btn-secondary">
                        문제 미리보기
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

이제 퀴즈 관련 기본 페이지들이 완성되었습니다! 다음에는 실제 퀴즈 응시 페이지와 결과 페이지를 만들어야 합니다.

## 7. 다음 TODO 참고

# 퀴즈 프로젝트 현재 상태 및 다음 단계

## 완성된 기능들

1. **홈페이지** - 최신 문제집, 카테고리, 학습 기록 표시
2. **문제집 목록** - 검색, 카테고리 필터링  
3. **문제집 상세보기** - 전체 문제와 정답 표시 (Quizlet의 기본 모드)
4. **퀴즈 시작 페이지** - 퀴즈 정보와 주의사항
5. **회원가입/로그인 시스템** - 사용자 인증 완료
6. **데이터베이스 모델** - CustomUser, QuestionSet, Question, Choice, Quiz 등
7. **관리자 페이지 설정** - Django Admin에서 데이터 관리 가능

## 아직 만들어야 할 페이지들

1. **퀴즈 응시 페이지** (`quiz_take.html`) - 실제 문제 풀기
2. **퀴즈 완료 페이지** (`quiz_complete.html`) - 결과 표시  
3. **내 퀴즈 기록** (`my_quizzes.html`) - 사용자 퀴즈 기록

## 다음 단계로 할 수 있는 것들

### 1. 관리자 페이지에서 테스트 데이터 추가 (우선순위 ⭐⭐⭐)
```bash
# 개발 서버 실행
python manage.py runserver

# 브라우저에서 http://127.0.0.1:8000/admin/ 접속
# 슈퍼유저로 로그인 후 데이터 추가:
```
- **카테고리** 추가 (예: 영어, 수학, 과학, 역사)
- **문제집** 생성 (각 카테고리별로 2-3개씩)  
- **문제와 선택지** 추가 (각 문제집당 5-10문제)

### 2. 퀴즈 응시 페이지 완성 (우선순위 ⭐⭐)
- JavaScript로 인터랙티브한 퀴즈 기능 구현
- AJAX를 통한 실시간 답안 제출
- 진행률 표시 및 타이머 기능

### 3. CSS 스타일링 개선 (우선순위 ⭐)
- Bootstrap 커스터마이징
- 더 예쁜 디자인 적용
- 모바일 반응형 최적화

## 추천 진행 순서

1. **먼저 관리자 페이지에서 테스트 데이터 추가**
   - 페이지들이 제대로 작동하는지 확인
   - 실제 데이터로 UI 테스트

2. **퀴즈 응시 페이지 완성**  
   - 핵심 기능 구현 완료

3. **스타일링 및 UX 개선**
   - 사용자 경험 향상

## 현재 파일 구조

```
프로젝트/
├── accounts/
│   ├── models.py
│   ├── views.py  
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── quiz/
│   ├── models.py
│   ├── views.py (일부 완성)
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── base/base.html
│   ├── accounts/
│   └── quiz/ (일부 완성)
├── static/css/style.css
└── db.sqlite3
```

## 다음 작업 체크리스트

- [ ] 관리자 페이지에서 테스트 데이터 추가
- [ ] 홈페이지 동작 확인  
- [ ] 문제집 목록/상세 페이지 테스트
- [ ] 퀴즈 응시 페이지 완성
- [ ] 퀴즈 완료 페이지 완성
- [ ] 내 퀴즈 기록 페이지 완성
- [ ] 전체 기능 테스트
- [ ] 스타일링 개선
