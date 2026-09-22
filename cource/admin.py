from django.contrib import admin
from .models import Cource,Enrollmentno
from accounts.models import User,ServiceProvider
# Register your models here.

@admin.register(Cource)
class CourceModel(admin.ModelAdmin):
    list_display=('provider','title','price','duration')
    search_fields=('title',)
    ordering=('-title',)

@admin.register(Enrollmentno)
class EnrollmentnoModel(admin.ModelAdmin):
    list_display=('user','cource','paid')
    search_fields=('cource',)
    ordering=('-cource',)

