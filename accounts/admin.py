from django.contrib import admin
from .models import User,ServiceProvider
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','email','phone')
    search_fields=('name','email')
    ordering=('name',)

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display=('id','name','company_name','email','phone')
    search_fields=('name','company_name','email')
    ordering=('name',)
