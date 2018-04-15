"""Murmur URL Configuration."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('murmur.myauth.urls', namespace="myauth"), ),
    path('oauth/', include('social_django.urls', namespace="social"), ),
    path('', include('murmur.web.urls', namespace="web")),
]
