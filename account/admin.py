from django.contrib import admin

# Register your models here.

from account.models import User, RegisterCache

admin.site.register(User)
admin.site.register(RegisterCache)