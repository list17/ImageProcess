from django.conf.urls import url
from .views import FindFaces


urlpatterns = [
    url(r'findfaces', FindFaces.as_view())
]