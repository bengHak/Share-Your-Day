from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('mypage/', views.mypage, name='mypage'),
    path('detail/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('register/create/', views.create, name='create'),
]
