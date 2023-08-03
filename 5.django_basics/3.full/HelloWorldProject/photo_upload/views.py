from django.shortcuts import render, redirect
from .models import Photo

def photo_upload(request):
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES['image']
        photo = Photo(title=title, image=image)
        photo.save()
        return redirect('photo_list')
    return render(request, 'photo_upload/photo_upload.html')

def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo_upload/photo_list.html', {'photos': photos})
