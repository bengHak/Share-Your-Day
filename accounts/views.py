from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    # if request.method == 'POST':
    #     if request.POST['password1']
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, login)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')
