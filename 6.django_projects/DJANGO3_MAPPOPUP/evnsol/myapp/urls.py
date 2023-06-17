from django.urls import path, reverse_lazy
from .views import login_view, logout_view, home_view
from .leds import led_view
from .locs import loc_view
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('led/', led_view, name='led'),
    path('loc/', loc_view, name='location'),
    path('', RedirectView.as_view(url=reverse_lazy('home')), name='root'),  # 빈 경로에 대한 리다이렉트
]
