from django.db import models
from account.models import User

# Create your models here.

class UserUpload(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='storages/uploads/%Y/%m/%d/')
    is_url = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)