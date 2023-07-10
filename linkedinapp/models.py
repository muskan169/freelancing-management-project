from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class JobPost(models.Model):
    JOB_STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    hourly_rate = models.CharField(max_length=10)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=JOB_STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f'{self.project.name} - {self.description}'

class JobProposal(models.Model):
    PROPOSAL_CHOICES = (
        ('OPEN', 'Open'),
        ('ENGAGED', 'Engaged'),
        ('REJECTED', 'Rejected'),
    )

    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    freelancer_hourly_rate = models.CharField(max_length=10)
    proposal_status = models.CharField(max_length=10, choices=PROPOSAL_CHOICES, default='OPEN')

    def __str__(self):
        return f"{self.freelancer} - {self.proposal_status}"
