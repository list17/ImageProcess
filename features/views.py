import face_recognition
from PIL import Image, ImageDraw

from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from io import BytesIO

from account.models import User
from .models import UserRecord
from .config import FeaturesDef
from filetransfer.models import UserUpload
# Create your views here.

class FaceEmoji(View):
    def post(self, request):
        # user = User.objects.get(username=request.POST['username'])
        user = User.objects.get(email='1511500409@qq.com')
        image = face_recognition.load_image_file(user.userupload.file)
        face_landmarks_list = face_recognition.face_landmarks(image)
        pil_image = Image.fromarray(image)
        for face_landmarks in face_landmarks_list:
            d = ImageDraw.Draw(pil_image, 'RGBA')

            d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
            d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
            d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
            d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

            d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
            d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
            d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
            d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

            d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
            d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

            d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
            d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)
        try:
            image_init = Image.open(user.userupload.file.url)
            buffer_init = BytesIO()
            image_init.save(fp=buffer_init, format=image_init.format)
            content_init = ContentFile(buffer_init.getvalue())
            thumb_init = InMemoryUploadedFile(content_init,None,user.userupload.file.url.split('/')[-1],'image/jpeg',content_init.tell, None)


            buffer_result = BytesIO()
            pil_image.save(fp=buffer_result,format=image_init.format)
            content_result = ContentFile(buffer_result.getvalue())
            thumb_result = InMemoryUploadedFile(content_result,None,'result' + user.userupload.file.url.split('/')[-1],'image/jpeg',content_result.tell, None)

            user_record = UserRecord.objects.create(features=FeaturesDef.face_emoji,
                                                    init_image=thumb_init,
                                                    result_image=thumb_result,
                                                    user=user)
        except Exception as e:
            print(e)
        return JsonResponse(data={"msg":"success",'url':'http://127.0.0.1:8080/api/filetransfer/storages?path='+user_record.result_image.url})
