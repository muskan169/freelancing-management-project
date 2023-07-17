from django.contrib import admin
from django.urls import path
from . import views
from .admin import ClientAdmin


urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('freelancer/dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('successsignup/', views.signup_view, name='signup'),
    path('create_project/', views.create_project, name='create_project'),
    path('project_dashboard/<int:project_id>/', views.project_dashboard, name='project_dashboard'),
    path('create_jobpost/<int:project_id>/', views.create_jobpost, name='create_jobpost'),
    path('create_jobproposal/<int:jobpost_id>/', views.create_jobproposal, name='create_jobproposal'),
    path('freelancer/jobproposals/<int:jobpost_id>/', views.job_proposal_list, name='job_proposal_list'),
    path('job_proposal_list/<int:jobpost_id>/', views.job_proposal_list, name='job_proposal_list'),
    path('accept_proposal/<int:proposal_id>/', views.accept_proposal, name='accept_proposal'),
    path('account_verification/', views.account_verification, name='account_verification'),
        path('verify_clients/<int:pk>/', views.verify_clients, name='verify_clients'),





]