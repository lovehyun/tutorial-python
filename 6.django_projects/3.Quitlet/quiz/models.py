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
