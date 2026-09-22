from django.db import models

# Create your models here.

class User(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    create_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    company_name=models.CharField(max_length=200)
    description=models.TextField()
    address=models.TextField()
    create_at=models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
