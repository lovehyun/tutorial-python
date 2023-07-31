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

6. 관리자 페이지 생성

    1. 관리자 계정 생성하기:
        Django의 관리자 페이지에 접근하기 위해서는 먼저 관리자 계정을 생성해야 합니다. Django는 기본적으로 createsuperuser 명령을 제공하여 관리자 계정을 생성할 수 있습니다.

        프로젝트 폴더에서 다음 명령을 실행하여 관리자 계정을 생성합니다.

        ```
        python manage.py createsuperuser
        ```
        이후, 원하는 사용자 이름, 이메일 주소, 비밀번호를 입력하고 엔터를 누릅니다.

    2. 관리자 페이지 설정:
        관리자 페이지를 사용하기 위해서는 admin 앱이 프로젝트에 등록되어 있어야 합니다. Django의 기본 설정 파일인 settings.py에 admin 앱이 등록되어 있는지 확인합니다.

        ```
        INSTALLED_APPS = [
            # ... 다른 앱들 ...
            'django.contrib.admin',
            # ...
        ]
        ```
        admin 앱이 등록되어 있지 않다면, 위와 같이 추가합니다.

    3. 서버 실행:
        관리자 페이지를 사용하기 위해서는 개발 서버를 실행해야 합니다. 프로젝트 폴더에서 다음 명령을 실행하여 개발 서버를 시작합니다.

        ``` 
        python manage.py runserver
        ```
        서버가 실행되면 브라우저에서 http://127.0.0.1:8000/admin/ 주소를 열어 관리자 페이지에 접속합니다.

    4. 로그인 및 관리:
        관리자 페이지에 접속하면 방금 생성한 관리자 계정으로 로그인을 요구합니다. 생성한 관리자 계정으로 로그인하면 관리자 페이지에서 사용자, 그룹, 권한, 데이터베이스 등을 관리할 수 있습니다.

        이제 관리자 페이지를 통해 Django 애플리케이션을 관리할 수 있습니다. 추가적으로 모델 클래스에 admin.py 파일을 생성하여 해당 모델을 관리자 페이지에서 보여지는 형식을 커스터마이즈할 수도 있습니다.
