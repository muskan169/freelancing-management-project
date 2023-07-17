from django.contrib import admin
from .models import Client, Freelancer, Project, JobPost, JobProposal
from django.shortcuts import render, redirect 
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import path
from django.urls import reverse
from django_object_actions import DjangoObjectActions


admin.site.register(Freelancer)
admin.site.register(Project)
admin.site.register(JobPost)
admin.site.register(JobProposal)

# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_verified')
#     actions = ['verify_clients']
#     list_filter = ["is_verified"]
    
#     def verify_clients(self, request, queryset):
#         queryset.update(is_verified=True)

#     verify_clients.short_description = "Verify selected clients"

class ClientAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name', 'is_verified')
    list_filter = ['is_verified']

    def verification_button(self, obj):
        if obj.is_verified:
            return 'Verified'
        else:
            url = reverse('admin:verify_clients', args=[obj.id])
            return format_html('<a class="button" href="{}">Verify</a>', url)

    verification_button.short_description = 'Verification'
    verification_button.allow_tags = True

    def verify_clients(self, request, queryset):
        queryset.update(is_verified=True)

    verify_clients.short_description = "Verify selected clients"
    change_actions = ('verify_clients',)

admin.site.register(Client, ClientAdmin)