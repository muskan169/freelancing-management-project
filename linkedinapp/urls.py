from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('freelancer/dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('successsignup/', views.signup_view, name='signup'),




]