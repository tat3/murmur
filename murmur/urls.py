"""Murmur URL Configuration."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('murmur.myauth.urls', namespace="myauth"), ),
]
