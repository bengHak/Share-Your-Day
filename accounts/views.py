from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# from .models import Profile
# from django.contrib.auth import get_user_model

# User = get_user_model


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                request.POST['username'], password=request.POST['password1'])
            # profile = Profile(user=user)
            # profile.save()
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match'})
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')
