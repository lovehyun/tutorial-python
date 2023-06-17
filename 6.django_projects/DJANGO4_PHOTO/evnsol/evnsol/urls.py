"""evnsol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import login_view, logout_view, home_view

import os


# URL_PREFIX 환경 변수를 가져옵니다.
url_prefix = settings.URL_PREFIX
print(f'Setting up the URL_PREFIX: {url_prefix}')

urlpatterns = [
    path(url_prefix + 'admin/', admin.site.urls),
    path(url_prefix + '', RedirectView.as_view(url=reverse_lazy('home')), name='root'),  # 빈 경로에 대한 리다이렉트
    path(url_prefix + 'login/', login_view, name='login'),
    path(url_prefix + 'logout/', logout_view, name='logout'),
    path(url_prefix + 'home/', home_view, name='home'),
    path(url_prefix + 'myapp/', include('myapp.urls')),  # myapp의 URL 패턴을 포함시킴
    path(url_prefix + 'photo/', include('photo.urls')),
] 

# 사진 업로드 폴더 추가 등록
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
