from django.urls import path
from .leds import led_view
from .locs import loc_view

urlpatterns = [
    path('led/', led_view, name='led'),
    path('loc/', loc_view, name='location'),
]
