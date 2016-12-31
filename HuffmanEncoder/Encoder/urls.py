from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = 'Encoder'

urlpatterns = [
    url(r'^encode/$', views.EncoderAPI.as_view()),
    url(r'^decode/$', views.DecoderAPI.as_view())
]
