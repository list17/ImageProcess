import random
import string

from django.db import models
from account.models import User

# Create your models here.
def rename(instace, filename):
    string_length=32
    letters = string.ascii_letters + string.digits
    return 'storages/uploads/' + ''.join(random.choice(letters) \
        for i in range(string_length)) + '.' + filename.split('.')[-1]

class UserUpload(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=rename)
    is_url = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
