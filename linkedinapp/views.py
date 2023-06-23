from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import models
from .models import Client, Freelancer, Project , JobPost , JobProposal
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404


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

def project_dashboard(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'project_dashboard.html', {'project': project})

def create_project(request):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        
        # Get the current user as the client
        client = Client.objects.get(user=request.user)

        # Create a new Project object
        project = Project.objects.create(client=client, name=project_name)

        # Redirect to the client dashboard 
        return redirect('client_dashboard')

    return render(request, 'create_project.html')

def create_jobpost(request, project_id):
    if request.method == 'POST':
        # Retrieve form data and create a new JobPost object
        project = Project.objects.get(id=project_id)
        description = request.POST['description']
        hourly_rate = request.POST['hourly_rate']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        status = request.POST['status']
        job_post = JobPost.objects.create(project=project, description=description, hourly_rate=hourly_rate, start_date=start_date, end_date=end_date, status=status)
        
        # Redirect to the project dashboard
        return redirect('project_dashboard', project_id=project_id)

    # If the request method is GET, retrieve the project object and render the create_jobpost.html template
    project = Project.objects.get(id=project_id)
    return render(request, 'create_jobpost.html', {'project': project})

def freelancer_dashboard(request):
    # Retrieve all the job posts
    job_posts = JobPost.objects.all()
    
    return render(request, 'freelancer_dashboard.html', {'job_posts': job_posts})

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

def create_jobproposal(request, jobpost_id):
    if request.method == 'POST':
        # Retrieve form data and create a new JobProposal object
        job_post = JobPost.objects.get(id=jobpost_id)
        freelancer = Freelancer.objects.get(user=request.user)
        freelancer_hourly_rate = request.POST['freelancer_hourly_rate']
        proposal_status = 'OPEN'  # Set the initial status as 'OPEN'
        
        job_proposal = JobProposal.objects.create(job_post=job_post, freelancer=freelancer, freelancer_hourly_rate=freelancer_hourly_rate, proposal_status=proposal_status)
        
        return redirect('freelancer_dashboard')

    # If the request method is GET, retrieve the job post object and render the create_jobproposal.html template
    job_post = JobPost.objects.get(id=jobpost_id)
    return render(request, 'create_jobproposal.html', {'job_post': job_post})

def job_proposal_list(request):
    # Retrieve the logged-in freelancer
    freelancer = Freelancer.objects.get(user=request.user)

    # Retrieve all job proposals submitted by the freelancer
    job_proposals = JobProposal.objects.filter(freelancer=freelancer)

    return render(request, 'jobproposal_list.html', {'job_proposals': job_proposals})
