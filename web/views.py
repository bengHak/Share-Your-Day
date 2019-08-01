from django.shortcuts import render


def about(request):
    return render(request, 'about.html')


def index(request):
    return render(request, 'index.html')


def mypage(request):
    return render(request, 'mypage.html')

def detail(request):
    fund_detail = {
        'title': '기부 제목',
        'content': '기부 내용~~~~~~~~~~~~~~~~~',
        'current_fund' : 560000,
        'goal' : 1000000,
        'max_fund' : -1,
        'min_fund' : 10,
        'image_url' : 'https://picsum.photos/400/400',
        'fund_id' : 1,
        'hit' : 96,
        'like' : 2019,
    }
    return render(request, 'detail.html', fund_detail)