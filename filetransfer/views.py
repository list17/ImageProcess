import re
import random
import string

from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import uri_to_iri, iri_to_uri
from PIL import Image

from .models import UserUpload
from account.models import User
from features.models import UserRecord
from features.config import FeaturesDef
# Create your views here.

class FileUpload(View):
    def post(self, request):
        user = User.objects.get(username=request.user.username)
        try:
            url = request.POST['is_url']
        except Exception as e:
            try:
                user.userupload.file = request.FILES['file']
            except Exception as e:
                print(e)
                return JsonResponse(data={'msg':e},status=400)
            user.userupload.save()
            return JsonResponse(data={"msg":"上传成功，之后请选择您需要对上传的图片需要进行的操作"},status=200)
        image = ImageDownload(request.POST.get('url'))
        image.show()
        return JsonResponse(data={"msg":"上传成功，之后请选择您需要对上传的图片需要进行的操作"},status=200)


class FileDownload(View):
    '''
    return the file the user needs
    '''
    def post(self, request):
        pass


def ImageDownload(url):
    pass


class GetImageByUrl(View):
    def get(self, request):
        path = request.GET['path']
        suffix = path.split('.')[-1]
        if suffix == 'png':
            content_type = 'image/png'
        elif suffix == 'jpeg':
            content_type = 'image/jpeg'
        elif suffix == 'jpg':
            content_type = 'image/jpg'
        else:
            return JsonResponse(data={"msg":"format error"},status=400)
        try:
            response = HttpResponse(content_type='image/png')
            image_data = Image.open(path)
            image_data.save(response,"PNG")
        except Exception as e:
            return JsonResponse(data={"msg":e},status=400)
        return response


class UserHistoryDownload(View):
    def post(self, request):
        if request.user.is_anonymous:
            return JsonResponse(data={"msg":"not login"}, status=400)
        user = User.objects.get(username=request.user.username)
        dataset = []
        filters = []
        for record in user.userrecord_set.all():
            try:
                filters.index({"text":record.date,"value":record.date})
            except ValueError:
                filters.append({"text":record.date,"value":record.date})
            if record.features == 1:
                feature = "一键\"美颜\""
            elif record.features == 2:
                feature = "暂时未定"
            dataset.append({'id': record.id, 'date': record.date, 'feature': feature, 'image':["http://127.0.0.1:8080/api/filetransfer/storages?path="+record.init_image.url,"http://127.0.0.1:8080/api/filetransfer/storages?path="+record.result_image.url]})
        return JsonResponse(data={'dataset':dataset,
                                    'filter':filters})


class DeleteRecords(View):
    def post(self, request):
        deletions = request.POST['deleterecords'].split(',')
        user = User.objects.get(username=request.user.username)
        records = user.userrecord_set.all()
        for record in records:
            try:
                index = deletions.index(str(record.id))
            except ValueError:
                continue
            record.delete()
        return JsonResponse(data={'msg':'delete successfully'})