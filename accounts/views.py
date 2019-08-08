from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from .models import Profile
from web.models import Register

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


# user_id = profile_id
def profile(request, profile_id):
    profileInfo = get_object_or_404(
        Profile, user=get_object_or_404(User, pk=profile_id))

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

    donation_list = []

    for fund1 in fund.donation_set.all().filter(user=profileInfo):
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
        donation_list.append(fund_detail)
    return render(request, 'profile.html', {'fund_list': fund_list, 'donation_list': donation_list, 'profileInfo': profileInfo})


def updateProfile(request, profile_id):
    updateProfile = get_object_or_404(
        Profile, user=get_object_or_404(User, pk=profile_id))
    return render(request, 'userupdate.html', {'updateProfile': updateProfile})


def editProfile(request, profile_id):
    edit = Profile.objects.get(user=get_object_or_404(User, pk=profile_id))

    # edit.user = request.POST['user']
    edit.nickname = request.POST['nickname']
    edit.phoneNumber = request.POST['phoneNumber']
    # edit.profileImage = request.POST['profileImage']
    edit.save()

    return redirect('index')
