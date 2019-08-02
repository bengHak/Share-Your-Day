from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('mypage/', views.mypage, name='mypage'),
    path('detail/<int:register_id>', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('register/create/', views.create, name='create'),
]
