from django.db import models
from account.models import User
from filetransfer.models import UserUpload
from .config import FeaturesDef
# Create your models here.

class UserRecord(models.Model):
    features = models.IntegerField(default=FeaturesDef.no_feature)
    data = models.DateTimeField(auto_now_add=True)
    upload = models.ForeignKey(UserUpload,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)