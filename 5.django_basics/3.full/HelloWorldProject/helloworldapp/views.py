from django.shortcuts import render
from .models import Message

# Create your views here.
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello, World!")

def show_messages(request):
    messages = Message.objects.all()
    return render(request, 'message_list.html', {'messages': messages})
