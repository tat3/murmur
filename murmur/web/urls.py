"""URL configuration for web page."""

from django.urls import path
from django.views.generic.base import TemplateView

from . import views
from .apps import WebConfig

app_name = WebConfig.name


urlpatterns = [
    path('', views.index, name="index"),
    path('update/', views.update, name="update"),
    path('error/', TemplateView.as_view(
        template_name="web/error.html"),
        name="error"),
]
