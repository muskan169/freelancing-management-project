from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import models
from .models import Client, Freelancer, Project , JobPost
from django.contrib.auth import authenticate, login
from django.contrib import messages




# Create your views here.
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if Client.objects.filter(user=user).exists():
                login(request, user)
                return redirect('client_dashboard')
            elif Freelancer.objects.filter(user=user).exists():
                login(request, user)
                return redirect('freelancer_dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def client_dashboard(request):
    projects = Project.objects.filter(client__user=request.user)
    return render(request, 'client_dashboard.html', {'projects': projects})

def create_project(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        
        # Get the current user as the client
        client = Client.objects.get(user=request.user)

        # Create a new Project object
        project = Project.objects.create(client=client, name=project_name)

        # Redirect to the client dashboard or display a success message
        return redirect('client_dashboard')

    return render(request, 'create_project.html')


def freelancer_dashboard(request):
    return render(request, 'freelancer_dashboard.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        signup_user = request.POST['signup_user']

        # Create a new User object
        user = User.objects.create_user(username=username, password=password)

        if signup_user == 'client':
            # Create a new Client object and link it to the User object
            client = Client.objects.create(user=user, name=username)
        elif signup_user == 'freelancer':
            # Create a new Freelancer object and link it to the User object
            freelancer = Freelancer.objects.create(user=user, name=username)

        return render(request, 'success_signup.html')



    return render(request, 'signup.html')

