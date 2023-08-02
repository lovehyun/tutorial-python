from django.apps import AppConfig


class HelloworldappConfig(AppConfig):
    # default_auto_field : 기본 자동 필드 설정값
    #   Django 3.2이후부터 추가된 기능으로, 
    #   BigAutoField 는 PK의 Auto Increment시 64비트 정수를 사용함
    #   이전 버전까지는 AutoField 로 32비트 정수를 사용함
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'helloworldapp'
