from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile


def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email']
            )
            try:
                email = request.POST['email']
                nickname = request.POST['nickname']
                birthday = request.POST['birthday']
                phoneNumber = request.POST['phoneNumber']
                profileImage = request.FILES['profileImage']

                profile = Profile(user=user, nickname=nickname, email=email,
                                  birthday=birthday, phoneNumber=phoneNumber, profileImage=profileImage)
                profile.save()
                auth.login(request, user)
                return redirect('index')
            except:
                user.delete()
                return redirect('signup')
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match'})
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        profile = get_object_or_404(Profile, email=email)

        if profile is not None:
            user = auth.authenticate(
                request, username=profile.user.username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error': 'username or password is incorrect.'})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')
