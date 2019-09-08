import re
import random
import string

from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import UserUpload
from account.models import User
# Create your views here.

class FileUpload(View):
    def post(self, request):
        # user needs to be changed
        user = User.objects.get(email='1511500409@qq.com')
        try:
            request.POST.get('is_url')
        except:
            try:
                UserUpload.objects.create(file=request.FILES['file'], user=user)
            except Exception as e:
                return JsonResponse(data={'msg':e},status=400)
            user.uploadnum += 1
            user.save()
            return JsonResponse(data={"msg":"上传成功，之后请选择您需要对上传的图片需要进行的操作"},status=200)
        image = ImageDownload(request.POST.get('url'))
        print(image)
        user.uploadnum += 1
        user.save()
        return JsonResponse(data={"msg":"上传成功，之后请选择您需要对上传的图片需要进行的操作"},status=200)


class FileDownload(View):
    '''
    return the file the user needs
    '''
    def post(self, request):
        pass


def ImageDownload(url):
    pass