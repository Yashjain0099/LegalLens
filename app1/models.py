from django.db import models

# Create your models here.
class signuppage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    date=models.DateField()
    
    
    def __str__(self):
        return self.email
    
    
