from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('detail/<int:fund_id>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('register/create/', views.create, name='create'),
    path('FAQ/', views.faq, name='faq'),
    path('like/<int:fund_id>/', views.post_like, name='post_like'),
    path('payment/', views.payment, name='payment'),
    path('pay/', views.pay, name='pay'),
    path('test-like', views.like, name='like'),
    path('Privacy/', views.Privacy, name='Privacy'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
