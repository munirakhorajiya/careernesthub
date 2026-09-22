from django.db import models
from accounts.models import User,ServiceProvider
# Create your models here.

class Job(models.Model):
    provider=models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    location=models.CharField(max_length=200)
    salary=models.CharField(max_length=200)
    skills=models.TextField()
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Internship(models.Model):
    provider=models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    stipend=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    duration=models.CharField(max_length=200)
    skills=models.TextField()
    created_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Application(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE,blank=True,null=True)
    internship=models.ForeignKey(Internship,on_delete=models.CASCADE,blank=True,null=True)
    status=models.CharField(max_length=50,default='Pending')
    applied_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.name
    

