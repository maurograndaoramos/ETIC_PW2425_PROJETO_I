from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import SignupView, Login

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('premium/', views.premium, name='premium'),
]