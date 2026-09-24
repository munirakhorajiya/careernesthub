from django.db import models
from accounts.models import User,ServiceProvider
# Create your models here.
class Cource(models.Model):
    provider=models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    duration=models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Enrollmentno(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cource=models.ForeignKey(Cource,on_delete=models.CASCADE)
    paid=models.CharField(max_length=200, default='unpaid', blank=True)

    class Meta:
        unique_together = ('user', 'cource')

    def __str__(self):
        return f"{self.user.name} - {self.cource.title}"
