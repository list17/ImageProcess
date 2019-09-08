from django.db import models
from account.models import User

# Create your models here.

class UserUpload(models.Model):
    uploadid = models.IntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    is_url = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)