from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),                               # /polls/
    path('<int:question_id>/', views.detail, name='detail'),           # /polls/5/
    path('<int:question_id>/results/', views.results, name='results'), # /polls/5/results/
    path('<int:question_id>/vote/', views.vote, name='vote'),          # /polls/5/vote/
]
