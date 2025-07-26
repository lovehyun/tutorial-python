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
