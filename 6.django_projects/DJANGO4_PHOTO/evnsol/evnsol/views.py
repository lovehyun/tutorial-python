from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 로그인 성공 시 리다이렉트할 URL
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    # 로그인된 사용자에게만 접근 허용
    username = request.user.username
    context = {
        'username': username,
    }
    return render(request, 'home.html', context)
