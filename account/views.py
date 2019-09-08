from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import re
import random
import string

from .models import User, RegisterCache

def randomString(stringLength=32):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Create your views here.
class Login(View):
    def post(self, request):
        """
        user login
        if user is already login returns login already
        """

        username = request.POST['username']
        password = request.POST['password']

        if re.search(r"@", username):
            # check whether the user exist
            try:
                username = User.objects.get(email=username).username
            except:
                return JsonResponse(data={"msg":"user does not exist"}, status=400)

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={"msg":"login success",
                                            "username":username,
                                            "password":password,
                                            "nickname":user.nickname},status=200)
            else:
                return JsonResponse(data={"msg":"wrong password"}, status=400)

        # check whether the user exist
        if not User.objects.filter(username=username).exists():
            return JsonResponse(data={"msg":"user does not exist"}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse(data={"msg":"login success",
                                        "username":username,
                                        "email":user.email,
                                        "nickname":user.nickname}, status=200)
        else:
            return JsonResponse(data={"msg":"wrong password"}, status=400)


class Register(View):
    def post(self, request):
        self.nickname = request.POST['nickname']
        self._password = request.POST['password']
        self.password = hashers.make_password(self._password)
        self.user_email = request.POST['email']
        self.token = randomString()
        self.link = 'http://127.0.0.1:8080/api/user/register_confirm?'+"token="+self.token
        if RegisterCache.objects.filter(email=self.user_email).exists():
            return JsonResponse(data={"msg":"email has been used"}, status=400)
        self.message = render_to_string('register_confirm.html',{
            "nickname":self.nickname,
            "link":self.link
        })
        email = EmailMultiAlternatives("注册确认",strip_tags(self.message),to=[self.user_email])
        try:
            email.attach_alternative(self.message, "text/html")
            email.send()
        except Exception as e:
            return JsonResponse(data={"msg":'邮件发送失败'}, status=400)
        RegisterCache.objects.create(password=self.password, nickname=self.nickname, token=self.token, email=self.user_email)
        return JsonResponse(data={"msg":"email send"},status=200)


class RegisterConfirm(View):
    def get(self, request):
        self.token = request.GET['token']
        try:
            user_cache = RegisterCache.objects.get(token=self.token)
        except:
            return HttpResponse("注册失败")
        user = User.objects.create(username=user_cache.token, email=user_cache.email)
        user.set_raw_password(user_cache.password)
        user.save()
        return HttpResponse("注册成功")