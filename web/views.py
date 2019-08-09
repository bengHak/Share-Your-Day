from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse

import json
import copy

from datetime import datetime, date
from .models import Register, Donation
from accounts.models import Profile


def about(request):
    return render(request, 'about.html')


def index(request):
    register_objects = Register.objects.all()
    donation_objects = Donation.objects.all()
    today_total_fund = 0
    for donation in donation_objects:
        if donation.created_at.date() == date.today():
            today_total_fund += donation.amount


    fund_list = []
    for fund in register_objects:
        end_at = fund.expireDate  # date 객체1
        today = date.today()
        fund_objects = {
            'title': fund.title,
            'content': fund.content,
            'current_fund': fund.currentAmount,
            'organizer': fund.organizer,
            'goal': fund.targetAmount,
            'max_fund': fund.maxValue,
            'min_fund': fund.minValue,
            'image_url': fund.contentImage,
            'fund_id': fund.id,
            'hit': fund.hit,
            'like': fund.like_count,
            'd_day': (today - end_at).days,
            'pub_date': fund.pub_date,
        }
        fund_list.append(fund_objects)

    fund_list.reverse()
    fund_list.sort(key=lambda x: x['current_fund'], reverse=True)
    popular_list = fund_list[:]
    fund_list.sort(key=lambda x: x['d_day'], reverse=True)
    recent_list = fund_list[:]
    for item in recent_list:
        if item['d_day'] > 0:
            recent_list.remove(item)
            recent_list.append(item)

    if len(fund_list) == 0:
        return render(request, 'index.html', {})

    return render(request, 'index.html', {'popular_list': popular_list, 'recent_list': recent_list, 'today_total_fund':today_total_fund})
# 'main_1':fund_list[0], 'main_2':fund_list[1], 'main_3':fund_list[2]


def faq(request):
    return render(request, 'FAQ.html')


def detail(request, fund_id):
    fund = get_object_or_404(Register, pk=fund_id)
    donation_list = []
    if fund.currentAmount != 0:
        for donation in fund.donation_set.all():
            donation_list.append(donation)
        donation_list.sort(key=lambda x: x.amount, reverse=True)

    fund_detail = {
        'title': fund.title,
        'content': fund.content,
        'current_date': fund.pub_date,
        'current_fund': fund.currentAmount,
        'organizer': fund.organizer,
        'organization': fund.organization,
        # 'current_fund': 57,
        'start_day': fund.pub_date,
        'end_day': fund.expireDate,
        'goal': fund.targetAmount,
        'max_fund': fund.maxValue,
        'min_fund': fund.minValue,
        'image_url': fund.contentImage,
        'fund_id': fund_id,
        'hit': fund.update_counter,
        'like': fund.like_count,
        'donations': donation_list,
    }
    return render(request, 'detail.html', {'fund_detail': fund_detail})


def payment(request):
    return render(request, 'payment.html')

def privacy(request):
    return render(request, 'privacy.html')

@login_required
@require_POST
def pay(request):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=request.user)
        fund_id = request.POST.get('pk', None)
        fund = get_object_or_404(Register, pk=fund_id)
        fund_pay, fund_pay_created = fund.donation_set.get_or_create(
            user=profile)

        fund.currentAmount += int(request.POST.get('amount'))
        fund_pay.amount += int(request.POST.get('amount'))

        fund.save()
        fund_pay.save()

    context = {'fund_amount': fund.currentAmount}
    return HttpResponse(json.dumps(context), content_type='application/json')


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
        fund = get_object_or_404(Register, pk=fund_id)

        fund_like, fund_like_created = fund.like_set.get_or_create(
            user=profile)

        if not fund_like_created:
            fund_like.delete()
            message = 'You disliked this'
        else:
            message = 'You liked this'

    context = {'likes_count': fund.like_count, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')
    # dic 형식을 json 형식으로 바꾸어 전달한다.


def register(request):
    if request.user.is_authenticated:
        return render(request, 'register-fund.html')
    else:
        return render(request, 'login.html')


# 기부 등록
@login_required
def create(request):
    register = Register()
    profile = get_object_or_404(Profile, user=request.user)
    register.title = request.POST['title']
    register.expireDate = request.POST['expireDate']
    register.organizer = profile
    register.organization = request.POST['organization']
    register.minValue = request.POST['minValue']
    register.maxValue = request.POST['maxValue']
    register.targetAmount = request.POST['targetAmount']
    register.content = request.POST['content'].encode("utf-8")
    register.contentImage = request.FILES['contentImage']

    register.save()
    return redirect('detail', fund_id=(register.id))
