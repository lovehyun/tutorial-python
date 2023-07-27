## Intro to 장고
장고에서 간단한 "Hello, World!" 예제를 보여드리겠습니다.

1. 프로젝트 생성
   
    먼저, Django 프로젝트를 생성합니다. 콘솔 또는 터미널에서 다음 명령을 실행합니다:
    ```
    django-admin startproject HelloWorldProject
    ```
    생성된 프로젝트 폴더로 이동합니다:
    ```
    cd HelloWorldProject
    ```

2. 앱 생성
   
    다음으로, "Hello, World!"를 출력할 앱을 생성합니다. 앱을 생성하려면 다음 명령을 실행합니다:
    ```
    python manage.py startapp helloworldapp
    ```
    HelloWorldProject/settings.py 파일을 열어서 INSTALLED_APPS 항목에 helloworldapp를 추가합니다:

    ```
    INSTALLED_APPS = [
        # ...
        'helloworldapp',
        # ...
    ]
    ```

3. 앱 코드 작성
   
    helloworldapp 폴더 안에 views.py 파일을 생성하고 다음과 같이 코드를 작성합니다:
    ```
    from django.http import HttpResponse

    def hello_world(request):
        return HttpResponse("Hello, World!")
    ```
    helloworldapp 폴더 안에 urls.py 파일을 생성하고 다음과 같이 코드를 작성합니다:

    ```
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.hello_world, name='hello_world'),
    ]
    ```

4. 앱 등록
   
    이제 프로젝트의 최상위 urls.py 파일(HelloWorldProject/urls.py)을 열어 다음과 같이 수정합니다:

    ```
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('helloworldapp.urls')),
    ]
    ```

5. 결과 확인
   
    개발 서버를 실행하여 "Hello, World!"를 확인합니다:

    ```
    python manage.py runserver
    ```
    서버를 실행한 뒤, 웹 브라우저에서 http://127.0.0.1:8000/로 접속하면 "Hello, World!" 메시지가 표시됩니다.

    이것으로 Django에서 간단한 "Hello, World!" 예제를 구현했습니다. Django에서는 이처럼 간단하게 웹 애플리케이션을 작성할 수 있으며, 이후에는 복잡한 애플리케이션을 개발할 때 Django의 강력한 기능들을 사용할 수 있습니다.
