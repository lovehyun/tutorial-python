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
