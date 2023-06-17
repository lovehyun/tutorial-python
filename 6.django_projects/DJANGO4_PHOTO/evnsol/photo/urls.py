from django.urls import path
from .views import UploadPhotoView
from .views import PhotoListView

app_name = 'photo'

urlpatterns = [
    path('upload/', UploadPhotoView.as_view(), name='upload'),
    path('album/', PhotoListView.as_view(), name='album'),
]
