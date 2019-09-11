from django.conf.urls import url
from .views import FaceEmoji, Segamentation


urlpatterns = [
    url(r'faceemoji', FaceEmoji.as_view()),
    url(r'segmentation', Segamentation.as_view())
]
