from django.contrib import admin

from .models import Client, Freelancer, Project, JobPost, JobProposal

admin.site.register(Client)
admin.site.register(Freelancer)
admin.site.register(Project)
admin.site.register(JobPost)
admin.site.register(JobProposal)
