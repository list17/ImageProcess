from django.db import models
from account.models import User
from filetransfer.models import UserUpload
from .config import FeaturesDef
# Create your models here.

class UserRecord(models.Model):
    date = models.DateField(auto_now_add=True)

    features = models.IntegerField(default=FeaturesDef.no_feature)
    init_image = models.FileField(upload_to='storages/init/%Y/%m/%d/')
    result_image = models.FileField(upload_to='storages/result/%Y/%m/%d/')
    user = models.ForeignKey(User,on_delete=models.CASCADE)