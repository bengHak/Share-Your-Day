from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from datetime import date
from .models import Register
from accounts.models import Profile


def about(request):
    return render(request, 'about.html')


def index(request):
    register_objects = Register.objects.all()
    fund_list = []
    end_at = date(2019, 8, 10)  # date 객체1
    today = date.today()
    for fund in register_objects:
        fund_objects = {
            'title': fund.title,
            'content': fund.content,
            'current_fund': 56,
            'goal': fund.targetAmount,
            'max_fund': fund.maxValue,
            'min_fund': fund.minValue,
            'image_url': fund.contentImage,
            'fund_id': fund.id,
            'hit': fund.hit,
            'like': fund.like_count,
            'd_day': (end_at - today).days + 1,
        }
        fund_list.append(fund_objects)
    fund_list.reverse()
    return render(request, 'index.html', {'fund_list': fund_list})


def mypage(request):
    return render(request, 'mypage.html')


def faq(request):
    return render(request, 'FAQ.html')

def detail(request, fund_id):
    fund = get_object_or_404(Register, pk=fund_id)

    giver_list = []
    for giver in fund.like_user_set.all():
        giver_list.append(giver)

    fund_detail = {
        'title': fund.title,
        'content': fund.content,
        # 'current_date': fund.pub_date,
        # 'current_fund': fund.currentAmount,
        'current_fund': 57,
        'goal': fund.targetAmount,
        'max_fund': fund.maxValue,
        'min_fund': fund.minValue,
        'image_url': 'https://picsum.photos/900/500',
        'fund_id': fund_id,
        'hit': fund.update_counter,
        'like': fund.like_count,
        'givers' : giver_list,
    }
    return render(request, 'detail.html', {'fund_detail': fund_detail})

def payment(request):
    return render(request, 'payment.html')

@login_required
def post_like(request, fund_id):
    fund = get_object_or_404(Register, pk=fund_id)
    profile = get_object_or_404(Profile, user=request.user)
    fund_like, fund_like_created = fund.like_set.get_or_create(user=profile)

    if not fund_like_created:
        fund_like.delete()
    return redirect('detail', fund_id=fund_id)


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
    register.contentImage = request.FILES['contentImage']

    register.save()
    return redirect('detail', fund_id=(register.id))
