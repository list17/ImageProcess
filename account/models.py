from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=32)
    uploadnum = models.IntegerField(default=0)
    def set_raw_password(self, password):
        self.password = password

class RegisterCache(models.Model):
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    token = models.CharField(max_length=32)