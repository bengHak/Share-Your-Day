from django.shortcuts import render


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')
