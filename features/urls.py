from django.conf.urls import url
from .views import FaceEmoji


urlpatterns = [
    url(r'faceemoji', FaceEmoji.as_view())
]
