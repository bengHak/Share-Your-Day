from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from .models import Profile
from web.models import Register
from django.http import HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_POST

import json
from datetime import date


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
                auth.login(request, user,
                           backend="django.contrib.auth.backends.ModelBackend")
                return redirect('index')
            except Exception as error:
                user.delete()
                print(error)
                return render(request, 'signup.html', {'error': error, 'error_code': 1})
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match', 'error_code': 2})
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


def checkemail(request):
    try:
        email = Profile.objects.get(email=request.GET['email'])
    except Exception as e:
        email = None
    result = {
        'result': 'success',
        # 'data' : model_to_dict(username)  # console에서 확인
        'data': "not exist" if email is None else "exist",
        # 'user_data' : username
    }
    return JsonResponse(result)

# user_id = profile_id


def profile(request, profile_id):
    profileInfo = get_object_or_404(
        Profile, user=get_object_or_404(User, pk=profile_id))

    # 주최기부
    fund = Register.objects.all().filter(organizer=profileInfo)
    fund_list = []

    for fund in fund:
        end_at = fund.expireDate
        today = date.today()
        fund_detail = {
            'title': fund.title,
            'content': fund.content,
            'current_date': fund.pub_date,
            'current_fund': fund.currentAmount,
            'organizer': fund.organizer,
            # 'current_fund': 57,
            'start_day': fund.pub_date,
            'end_day': fund.expireDate,
            'goal': fund.targetAmount,
            'max_fund': fund.maxValue,
            'min_fund': fund.minValue,
            'image_url': fund.contentImage,
            'fund_id': fund.id,
            'hit': fund.update_counter,
            'like': fund.like_count,
            'd_day': (today - end_at).days,
            'pub_date': fund.pub_date,
        }
        fund_list.append(fund_detail)

 # 참가기부
 # fund1_list=[]
 # for fund1 in range(1,Register.objects.count()+1):
 #    fund1_list.append(fund1)
    # 프로필 주인의 총 기부금액과 기부 횟수
    total_fund = 0
    total_fund_count = 0

    do_user_list = []
    for i in range(1, Register.objects.count()+1):
        donation_list = []
        fund2 = get_object_or_404(Register, pk=i)  # register title
        for donation in fund2.donation_set.all():
            donation_list.append(donation)
        for dona in donation_list:
            if dona.user.user.id == profile_id:
                total_fund += dona.amount
                total_fund_count += 1
                fund_detail2 = {
                    'title': fund2.title,
                    'content': fund2.content,
                    'current_date': fund2.pub_date,
                    'current_fund': fund2.currentAmount,
                    'organizer': fund2.organizer,
                    # 'current_fund': 57,
                    'start_day': fund2.pub_date,
                    'end_day': fund2.expireDate,
                    'goal': fund2.targetAmount,
                    'max_fund': fund2.maxValue,
                    'min_fund': fund2.minValue,
                    'image_url': fund2.contentImage,
                    'fund_id': fund2.id,
                    'hit': fund2.update_counter,
                    'like': fund2.like_count,
                    'd_day': (today - end_at).days,
                    'pub_date': fund2.pub_date,
                }
                do_user_list.append(fund_detail2)

    if len(fund_list) == 0 and len(do_user_list) == 0:
        return render(request, 'profile.html', {'profileInfo': profileInfo})
    elif len(fund_list) == 0:
        return render(request, 'profile.html', {'profileInfo': profileInfo, 'do_user_list': do_user_list})
    elif len(do_user_list) == 0:
        return render(request, 'profile.html', {'profileInfo': profileInfo, 'fund_list': fund_list})

    return render(request, 'profile.html', {'fund_list': fund_list, 'do_user_list': do_user_list, 'profileInfo': profileInfo, 'total_fund': total_fund, 'total_fund_count': total_fund_count})


def updateProfile(request, profile_id):
    updateProfile = get_object_or_404(
        Profile, user=get_object_or_404(User, pk=profile_id))
    return render(request, 'userupdate.html', {'updateProfile': updateProfile})


def editProfile(request, profile_id):
    edit = Profile.objects.get(user=get_object_or_404(User, pk=profile_id))

    # edit.user = request.POST['user']
    edit.nickname = request.POST['nickname']
    edit.phoneNumber = request.POST['phoneNumber']
    edit.profileImage = request.FILES['profileImage']
    edit.save()

    return redirect('index')

@require_POST
def check_nickname(request):
    if request.method == 'POST':
        # user = request.user # 로그인한 유저를 가져온다.
        profiles = Profile.objects.all()
        
        for profile in profiles:
            print(profile.nickname)
            print(request.POST.get('nickname'))
            if profile.nickname == request.POST.get('nickname'):
                context = {'isExist': 1}
                return HttpResponse(json.dumps(context), content_type='application/json')
        
        context = {'isExist': 0}
        return HttpResponse(json.dumps(context), content_type='application/json')

@require_POST
def check_email(request):
    if request.method == 'POST':
        # user = request.user # 로그인한 유저를 가져온다.
        profiles = Profile.objects.all()
        
        for profile in profiles:
            print(profile.email)
            print(request.POST.get('email'))
            if profile.email == request.POST.get('email'):
                context = {'isExist': 1}
                return HttpResponse(json.dumps(context), content_type='application/json')
        
        context = {'isExist': 0}
        return HttpResponse(json.dumps(context), content_type='application/json')