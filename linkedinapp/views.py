from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import models
from .models import Client, Freelancer, Project , JobPost , JobProposal
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .permissions import client_required, freelancer_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect




# Create your views here.
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')


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

def account_verification(request):
    return render(request, 'account_verification.html')

@client_required
def client_dashboard(request):
    if hasattr(request.user, 'client'):
        client = request.user.client
        if client.is_verified:
            projects = Project.objects.filter(client=client)
            return render(request, 'client_dashboard.html', {'projects': projects})
        else:
            return render(request, 'account_verification.html')
    else:
        return redirect('home')

@client_required
def project_dashboard(request, project_id):
    if hasattr(request.user, 'client'):
        # project = Project.objects.get(Project, id=project_id, client__user=request.user)
        project = Project.objects.get(id=project_id, client__user=request.user)

        job_proposals = JobProposal.objects.filter(job_post__project=project)
        return render(request, 'project_dashboard.html', {'project': project, 'job_proposals': job_proposals})
    else:
        return redirect('home')

@client_required
def create_project(request):
    if hasattr(request.user, 'client'):
        if request.method == 'POST':
            project_name = request.POST['project_name']
            
            # Get the current user as the client
            client = request.user.client
    
            # Create a new Project object
            project = Project.objects.create(client=client, name=project_name)
    
            # Redirect to the client dashboard 
            return redirect('client_dashboard')
    
        return render(request, 'create_project.html')
    else:
        return redirect('home')


@client_required
def create_jobpost(request, project_id):
    if hasattr(request.user, 'client'):
        project = Project.objects.get(id=project_id, client__user=request.user)
        
        if request.method == 'POST':
            # Retrieve form data and create a new JobPost object
            description = request.POST['description']
            hourly_rate = request.POST['hourly_rate']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            status = request.POST['status']
            job_post = JobPost.objects.create(project=project, description=description, hourly_rate=hourly_rate, start_date=start_date, end_date=end_date, status=status)
            
            # Redirect to the project dashboard
            return redirect('project_dashboard', project_id=project_id)

        return render(request, 'create_jobpost.html', {'project': project})
    else:
        return redirect('home')


@freelancer_required
def freelancer_dashboard(request):
    if hasattr(request.user, 'freelancer'):
        # Retrieve all the job posts
        job_posts = JobPost.objects.all()
        return render(request, 'freelancer_dashboard.html', {'job_posts': job_posts})
    else:
        return redirect('home')
    
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

@freelancer_required
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


# @freelancer_required
@client_required
def job_proposal_list(request, jobpost_id):
    
    # Retrieve the job proposals for the specific job post
    job_proposals = JobProposal.objects.filter(job_post_id=jobpost_id)

    context = {
        'job_proposals': job_proposals,
    }
    return render(request, 'job_proposal_list.html', context)


@login_required(login_url='login')
def accept_proposal(request, proposal_id):
    proposal = JobProposal.objects.get(id=proposal_id)

    if proposal.proposal_status == 'OPEN':
        proposal.proposal_status = 'ACCEPTED'
        proposal.save()

        # Reject all other proposals for the same job post
        other_proposals = JobProposal.objects.filter(job_post=proposal.job_post).exclude(id=proposal_id)
        for other_proposal in other_proposals:
            other_proposal.proposal_status = 'REJECTED'
            other_proposal.save()

    return redirect('job_proposal_list', jobpost_id=proposal.job_post.id)

def verify_clients(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.is_verified = True
    client.save()
    return HttpResponseRedirect(reverse('admin:linkedinapp_client_changelist'))