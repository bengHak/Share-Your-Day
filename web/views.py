from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from .models import Register


def about(request):
    return render(request, 'about.html')


def index(request):
    return render(request, 'index.html')


def mypage(request):
    return render(request, 'mypage.html')


def detail(request):
    # fund_detail = get_object_or_404(Register, pk=register_id)
    fund_detail = {
        'title': '기부 제목',
        'content': '기부 내용',
        'current_fund': 560000,
        'goal': 1000000,
        'max_fund': -1,
        'min_fund': 10,
        'image_url': 'https://picsum.photos/400/400',
        'fund_id': 1,
        'hit': 96,
        'like': 2019,
    }
    return render(request, 'detail.html', fund_detail)


def register(request):
    if request.user.is_authenticated:
        return render(request, 'register-fund.html')
    else:
        return render(request, 'login.html')


# 기부 등록
def create(request):
    register = Register()
    register.title = request.POST['title']
    register.expireDate = request.POST['expireDate']
    register.organization = request.POST['organization']
    register.minValue = request.POST['minValue']
    register.maxValue = request.POST['maxValue']
    register.targetAmount = request.POST['targetAmount']
    register.content = request.POST['content']

    register.save()
    return redirect('index')
