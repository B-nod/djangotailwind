from django.urls import path
from . views import *
urlpatterns = [
    path('', homepage, name='homepage'),
    path('register', user_register, name='register'),
    path('login', user_login, name='login')
]