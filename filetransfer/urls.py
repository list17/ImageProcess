from django.conf.urls import url
from .views import FileUpload, GetImageByUrl, UserHistoryDownload, DeleteRecords

urlpatterns = [
    url(r'upload',FileUpload.as_view()),
    url(r'storages',GetImageByUrl.as_view()),
    url(r'download_user_history',UserHistoryDownload.as_view()),
    url(r'deleterecords', DeleteRecords.as_view())
]