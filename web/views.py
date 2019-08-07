from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json

from datetime import date
from .models import Register
from accounts.models import Profile


def about(request):
    return render(request, 'about.html')


def index(request):
    register_objects = Register.objects.all()
    fund_list = []
    for fund in register_objects:
        end_at = fund.expireDate  # date 객체1
        today = date.today()
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
        'start_day': fund.pub_date,
        'end_day': fund.expireDate,
        'goal': fund.targetAmount,
        'max_fund': fund.maxValue,
        'min_fund': fund.minValue,
        'image_url': fund.contentImage,
        'fund_id': fund_id,
        'hit': fund.update_counter,
        'like': fund.like_count,
        'givers': giver_list,
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

@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        # user = request.user # 로그인한 유저를 가져온다.
        profile = get_object_or_404(Profile, user=request.user)
        fund_id = request.POST.get('pk', None)
        fund = get_object_or_404(Register, pk=fund_id)#해당 메모 오브젝트를 가져온다.

        fund_like, fund_like_created = fund.like_set.get_or_create(user=profile)

        if not fund_like_created:
            fund_like.delete()
            message = 'You disliked this'   
        else:
            message = 'You liked this'

    context = {'likes_count' : fund.like_count, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')
    # dic 형식을 json 형식으로 바꾸어 전달한다.

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
