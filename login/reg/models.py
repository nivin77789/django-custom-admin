from django.db import models

# Create your models here.
class Logdetails(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=100)