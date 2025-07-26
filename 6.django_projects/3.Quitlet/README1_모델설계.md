# Quizlet 클론 모델 설계

## 1. accounts/models.py - 사용자 확장

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """사용자 모델 확장"""
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
```

## 2. quiz/models.py - 퀴즈 관련 모델

```python
# quiz/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Category(models.Model):
    """문제 카테고리"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class QuestionSet(models.Model):
    """문제집 (Quizlet의 Study Set과 같은 개념)"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_sets')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('quiz:question_set_detail', kwargs={'pk': self.pk})
    
    def get_question_count(self):
        return self.questions.count()

class Question(models.Model):
    """개별 문제"""
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_image = models.ImageField(upload_to='questions/', blank=True, null=True)
    explanation = models.TextField(blank=True, help_text="정답 해설")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.question_set.title} - Q{self.order}"

class Choice(models.Model):
    """선택지 (4지선다)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question} - {self.choice_text[:50]}"

class Quiz(models.Model):
    """퀴즈 세션 (시험 모드)"""
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    time_taken = models.DurationField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def get_percentage_score(self):
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100, 1)
        return 0

class QuizResult(models.Model):
    """개별 문제 답안 결과"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    time_taken = models.DurationField(null=True, blank=True)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['quiz', 'question']
    
    def __str__(self):
        return f"{self.quiz} - {self.question} - {'O' if self.is_correct else 'X'}"

class StudyProgress(models.Model):
    """학습 진도 추적"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    last_studied = models.DateTimeField(auto_now=True)
    times_studied = models.PositiveIntegerField(default=1)
    best_score = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'question_set']
    
    def __str__(self):
        return f"{self.user.username} - {self.question_set.title}"
```

## 3. settings.py 수정

```python
# settings.py에 추가
AUTH_USER_MODEL = 'accounts.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'quiz',
]
```

## 4. admin.py 설정

### accounts/admin.py
```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('profile_image',)}),
    )
```

### quiz/admin.py
```python
# quiz/admin.py
from django.contrib import admin
from .models import Category, QuestionSet, Question, Choice, Quiz, QuizResult, StudyProgress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    max_num = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'question_set', 'order']
    list_filter = ['question_set', 'created_at']
    search_fields = ['question_text']
    inlines = [ChoiceInline]

@admin.register(QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'is_public', 'get_question_count', 'created_at']
    list_filter = ['category', 'is_public', 'created_at']
    search_fields = ['title', 'description']
    
    def get_question_count(self, obj):
        return obj.get_question_count()
    get_question_count.short_description = '문제 수'

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'question_set', 'score', 'total_questions', 'get_percentage_score', 'is_completed']
    list_filter = ['is_completed', 'started_at']
    search_fields = ['title', 'user__username']

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']

@admin.register(StudyProgress)
class StudyProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'question_set', 'times_studied', 'best_score', 'last_studied']
    list_filter = ['last_studied']
```

## 5. 마이그레이션 실행

```bash
# 마이그레이션 파일 생성
python manage.py makemigrations accounts
python manage.py makemigrations quiz

# 마이그레이션 적용
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

## 6. 모델 관계도

```
User (CustomUser)
├── QuestionSet (creator)
├── Quiz (user)
└── StudyProgress (user)

QuestionSet
├── Questions (1:N)
├── Quiz (1:N)
└── StudyProgress (1:N)

Question
├── Choices (1:N)
└── QuizResult (1:N)

Quiz
└── QuizResults (1:N)
```

이제 Django 관리자 페이지에서 카테고리, 문제집, 문제들을 관리할 수 있고, 다음 단계로 뷰와 템플릿을 만들 수 있습니다!

## 7. Migration 이슈 발생 시
Django의 기본 admin 마이그레이션이 이미 실행되었는데, 나중에 CustomUser를 추가해서 발생한 문제입니다.

해결 방법 (데이터베이스 초기화):
```bash
# 1. 데이터베이스 파일 삭제
del db.sqlite3

# 2. 마이그레이션 파일들 삭제 (accounts 앱의)
del accounts\migrations\0001_initial.py
# __pycache__ 폴더도 삭제해주세요

# 3. 처음부터 다시 마이그레이션
python manage.py makemigrations accounts
python manage.py makemigrations quiz
python manage.py migrate

# 4. 슈퍼유저 다시 생성
python manage.py createsuperuser
```
