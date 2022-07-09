from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)

        if user:
            login(request, user)
            return redirect('inicioA')

        else:
            return render(request, 'user/login.html', {'error': 'el usuario no existe'})

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('inicioA')

    return render(request, 'user/login.html')


def log_out(request):
    logout(request)

    return redirect('inicioC')

