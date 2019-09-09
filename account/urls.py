from django.conf.urls import url
from .views import Login, Register, RegisterConfirm, Logout


urlpatterns = [
    url(r"login", Login.as_view()),
    url(r'register_confirm', RegisterConfirm.as_view()),
    url(r'register', Register.as_view()),
    url(r'logout', Logout.as_view()),
]