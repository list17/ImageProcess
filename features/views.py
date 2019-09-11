import skimage
import torch
import os
import face_recognition
import numpy as np
import torchvision.models as models
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw

from account.models import User
from .models import UserRecord
from .config import FeaturesDef
from filetransfer.models import UserUpload
from .imagenet import labels
# Create your views here.

class FaceEmoji(View):
    def post(self, request):
        if request.user.is_anonymous:
            return JsonResponse(data={'msg':"not login"},status=400)
        user = User.objects.get(username=request.user.username)
        try:
            image = face_recognition.load_image_file(user.userupload.file.url)
            face_landmarks_list = face_recognition.face_landmarks(image)
            pil_image = Image.fromarray(image)
            for face_landmarks in face_landmarks_list:
                image_draw = ImageDraw.Draw(pil_image, 'RGBA')

                image_draw.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
                image_draw.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
                image_draw.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
                image_draw.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

                image_draw.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
                image_draw.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
                image_draw.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
                image_draw.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

                image_draw.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
                image_draw.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

                image_draw.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
                image_draw.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

            image_init = Image.open(user.userupload.file.url)
            buffer_init = BytesIO()
            image_init.save(fp=buffer_init, format=image_init.format)
            content_init = ContentFile(buffer_init.getvalue())
            thumb_init = InMemoryUploadedFile(content_init,None,user.userupload.file.url.split('/')[-1],'image/jpeg',content_init.tell, None)


            buffer_result = BytesIO()
            pil_image.save(fp=buffer_result, format=image_init.format)
            content_result = ContentFile(buffer_result.getvalue())
            thumb_result = InMemoryUploadedFile(content_result,None,'result' + user.userupload.file.url.split('/')[-1],'image/jpeg',content_result.tell, None)

            user_record = UserRecord.objects.create(features=FeaturesDef.face_emoji,
                                                    init_image=thumb_init,
                                                    result_image=thumb_result,
                                                    user=user)
        except Exception as e:
            print(e)
        return JsonResponse(data={"msg":"success",'url':'http://127.0.0.1:8080/api/filetransfer/storages?path='+user_record.result_image.url})


class Segamentation(View):
    def post(self, request):
        if request.user.is_anonymous:
            return JsonResponse(data={'msg':"not login"},status=400)
        user = User.objects.get(username=request.user.username)
        try:
            image = skimage.io.imread(user.userupload.file.url)
            # image = skimage.transform.resize(image, (520, 520), anti_aliasing=True)
            image = np.transpose(image, (2, 0, 1))
            image = image.astype(np.float32)
            input_np = torch.from_numpy(image)

            normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                std=[0.229, 0.224, 0.225])
            input_np = normalize(input_np)
            input_np = torch.unsqueeze(input_np, 0)

            fcn_resnet101 = models.segmentation.fcn_resnet101(pretrained=True)
            fcn_resnet101.eval()

            output = fcn_resnet101(input_np)['out'].squeeze(0).argmax(0)
            plt.imsave(user.userupload.file.url.split('/')[-1], output)

            image_init = Image.open(user.userupload.file.url)
            buffer_init = BytesIO()
            image_init.save(fp=buffer_init, format=image_init.format)
            content_init = ContentFile(buffer_init.getvalue())
            thumb_init = InMemoryUploadedFile(content_init,None,user.userupload.file.url.split('/')[-1],'image/jpeg',content_init.tell, None)

            image_result = Image.open(user.userupload.file.url.split('/')[-1])

            buffer_result = BytesIO()
            image_result.save(fp=buffer_result,format=image_init.format)
            content_result = ContentFile(buffer_result.getvalue())
            thumb_result = InMemoryUploadedFile(content_result,None,'result' + user.userupload.file.url.split('/')[-1],'image/jpeg',content_result.tell, None)

            user_record = UserRecord.objects.create(features=FeaturesDef.segmentation,
                                                    init_image=thumb_init,
                                                    result_image=thumb_result,
                                                    user=user)

            os.remove(user.userupload.file.url.split('/')[-1])

            return JsonResponse(data={"msg":"success","url":"http://127.0.0.1:8080/api/filetransfer/storages?path=" + user_record.result_image.url})
        except Exception as e:
            print(e)
            return JsonResponse(data={"msg":"error"}, status=400)