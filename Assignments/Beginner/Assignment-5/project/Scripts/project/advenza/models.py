from django.db import models

# Create your models here.
class advenza_user(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
