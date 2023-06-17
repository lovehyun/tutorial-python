from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views import View
from .forms import PhotoForm

from django.views.generic import ListView
from .models import Photo


class UploadPhotoView(View):
    def get(self, request):
        form = PhotoForm()
        return render(request, 'photo/upload.html', {'form': form})

    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'photo/success.html')
        return render(request, 'photo/upload.html', {'form': form})


class PhotoListView(ListView):
    model = Photo
    template_name = 'photo/album.html'
    context_object_name = 'photos'
