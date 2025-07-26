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
