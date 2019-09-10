import re
import random
import string
import requests

from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse,FileResponse
from django.views.generic import View
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import uri_to_iri, iri_to_uri
from django.core.files import File
from PIL import Image
from os.path import basename
from tempfile import TemporaryFile
from urllib.parse import urlsplit

from .models import UserUpload
from account.models import User
from features.models import UserRecord
from features.config import FeaturesDef
# Create your views here.

class FileUpload(View):
    def post(self, request):
        if request.user.is_anonymous:
            return JsonResponse(data={'msg':"not login"},status=400)
        try:
            user = User.objects.get(username=request.user.username)
            try:
                url = request.POST['url']
            except Exception as e:
                try:
                    user.userupload.file = request.FILES['file']
                except Exception as e:
                    return JsonResponse(data={'msg':"error"},status=400)
                user.userupload.save()
                return JsonResponse(data={"msg":"上传成功，之后请选择您需要对上传的图片需要进行的操作"},status=200)
            download_to_file_field(url, user.userupload.file)
        except Exception as e:
            return JsonResponse(data={'msg':'error'},status=400)
        return JsonResponse(data={"msg":"上传成功，之后请选择您需要对上传的图片需要进行的操作"},status=200)

class FileDownload(View):
    '''
    return the file the user needs
    '''
    def get(self, request):
        try:
            filepath = request.GET['path'].split('=')[-1]
            suffix = filepath.split('.')[-1]
            if suffix == 'png':
                content_type = 'image/png'
                save_type = "PNG"
            elif suffix == 'jpeg':
                content_type = 'image/jpeg'
                save_type = "JPEG"
            elif suffix == 'jpg':
                content_type = 'image/jpg'
                save_type = "JPEG"
            image = Image.open(filepath)
            response = HttpResponse(content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filepath.split('/')[-1])
            image.save(response, save_type)
            return response
        except Exception as e:
            print(e)
            return JsonResponse(data={"msg":"error"},status=400)

def download_to_file_field(url, field):
    with TemporaryFile() as tf:
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=4096):
            tf.write(chunk)
        tf.seek(0)
        field.save(basename(urlsplit(url).path), File(tf))


class GetImageByUrl(View):
    def get(self, request):
        path = request.GET['path']
        suffix = path.split('.')[-1]
        if suffix == 'png':
            content_type = 'image/png'
            save_type = "PNG"
        elif suffix == 'jpeg':
            content_type = 'image/jpeg'
            save_type = "JPEG"
        elif suffix == 'jpg':
            content_type = 'image/jpg'
            save_type = "JPEG"
        else:
            return JsonResponse(data={"msg":"format error"},status=400)
        try:
            response = HttpResponse(content_type=content_type)
            image_data = Image.open(path)
            image_data.save(response,save_type)
        except Exception as e:
            return JsonResponse(data={"msg":'error'},status=400)
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
        if request.user.is_anonymous:
            return JsonResponse(data={'msg':"not login"},status=400)
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