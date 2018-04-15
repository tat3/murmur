"""URL configuration for web page."""

from django.urls import path

from . import views
from .apps import WebConfig

app_name = WebConfig.name


urlpatterns = [
    path('', views.index, name="index"),
]
