import face_recognition
from django.contrib.auth import authenticate, login, logout, tokens, hashers
from django.http import HttpResponse, JsonResponse
from django.views.generic import View


# Create your views here.

class FindFaces(View):
    def post(self, request):
        image = face_recognition.load_image_file("/home/list/Pictures/wallpapers/42c65360-025d-11e7-94ea-b12f28cb34b4.png")
        face_locations = face_recognition.face_locations(image)
        print(face_locations)
        return JsonResponse(data={"msg":"hello"})