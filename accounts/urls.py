from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:profile_id>', views.profile, name='profile'),
    path('profile/update/<int:profile_id>',
         views.updateProfile, name='updateProfile'),
    path('profile/edit/<int:profile_id>',
         views.editProfile, name='editProfile'),
     path('checkemail', views.checkemail),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
