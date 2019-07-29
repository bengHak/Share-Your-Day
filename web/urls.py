from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('mypage/', views.mypage, name='mypage'),
]
