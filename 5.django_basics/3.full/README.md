## TODO 앱 만들기

장고(Django)로 가장 쉽게 연습해볼 수 있는 예시 앱은 "To-Do List" 앱입니다. 이 앱은 할 일 목록을 관리하는 기능을 갖추고 있어 간단하면서도 실제로 사용할 수 있는 기능을 구현할 수 있습니다. 아래는 "To-Do List" 앱의 예시 코드입니다.

1. 앱 생성:
    
    ```
    $ django-admin startapp todo
    ```
    앱을 생성하고 installed_app 에 추가한다.
    
2. 모델 정의: **`todo/models.py`** 파일에 다음과 같이 모델을 정의합니다.
    
    ```
    from django.db import models
    
    class Task(models.Model):
        title = models.CharField(max_length=200)
        completed = models.BooleanField(default=False)
    
        def __str__(self):
            return self.title
    ```
    
3. 데이터베이스 마이그레이션:
    
    ```
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```
    
4. 뷰 함수 작성: **`todo/views.py`** 파일에 다음과 같이 뷰 함수를 작성합니다.
    
    ```
    from django.shortcuts import render
    from .models import Task
    
    def task_list(request):
        tasks = Task.objects.all()
        return render(request, 'todo/task_list.html', {'tasks': tasks})
    ```
    
5. 템플릿 작성: **`todo/templates/todo/task_list.html`** 파일을 생성하고 다음과 같이 작성합니다.
    
    ```
    <h1>To-Do List</h1>
    
    <ul>
        {% for task in tasks %}
            <li>{{ task.title }}</li>
        {% endfor %}
    </ul>
    ```
    
6. URL 매핑: 프로젝트의 **`urls.py`** 파일에 URL 매핑을 설정합니다.
    
    ```
    from django.urls import path
    from todo.views import task_list
    
    urlpatterns = [
        path('tasks/', task_list, name='task_list'),
    ]
    ```
    
7. 개발 서버 실행:
    
    ```
    $ python manage.py runserver
    ```
    
    이제 웹 브라우저에서 **`http://localhost:8000/tasks/`** 주소로 접속하면 할 일 목록이 나열되는 페이지를 볼 수 있습니다. 이 예시를 기반으로 추가적인 기능을 구현하거나 디자인을 개선해볼 수 있습니다.
    
8. 관리자 페이지 추가
    
    Django의 admin 페이지에도 **`todo`** 앱에 대한 내용을 추가할 수 있습니다. Django의 admin 기능은 관리자를 위한 편리한 인터페이스를 제공하며, 데이터베이스의 내용을 관리할 수 있습니다.
    
    **`todo/admin.py`** 파일을 열고 다음과 같이 내용을 추가해보겠습니다:
    
    ```
    from django.contrib import admin
    from .models import Task
    
    admin.site.register(Task)
    ```
    
    위 코드는 **`Task`** 모델을 admin 페이지에서 관리할 수 있도록 등록하는 역할을 합니다.
    
    이제 웹 브라우저에서 **`http://localhost:8000/admin/`** 주소로 접속하면 Django의 admin 페이지가 나타납니다. admin 페이지에 로그인하고 **`Tasks`** 항목을 클릭하면 할 일 목록을 관리할 수 있는 인터페이스를 사용할 수 있습니다. 여기서 할 일을 추가, 수정, 삭제할 수 있습니다.