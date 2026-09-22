from django.contrib import admin
from .models import Job,Internship,Application
# Register your models here.

@admin.register(Job)
class JobModel(admin.ModelAdmin):
    list_display=('id','title','provider','location','salary','created_at')
    search_fields=('title','location','skills')
    list_filter=('location',)
    ordering=('-created_at',)

@admin.register(Internship)
class InternshipModel(admin.ModelAdmin):
    list_display=('id','title','provider','location','stipend','duration','created_at')
    search_fields=('title','location','skills')
    list_filter=('location',)
    ordering=('-created_at',)

@admin.register(Application)
class ApplicationModel(admin.ModelAdmin):
    list_display=('id','user','job','internship','status','applied_date')
    search_fields=('user__name','user__email')
    list_filter=('status',)
    ordering=('-applied_date',)

