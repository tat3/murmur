"""
URL configurations for login/logout.

Using default views produced by auth.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

from .apps import MyauthConfig

app_name = MyauthConfig.name


urlpatterns = [
    # path('', views.index, name="index"),
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),
    path('login/', auth_views.login,
         {"template_name": 'myauth/login.html'},
         name="login"),
    path('logout/', auth_views.logout, name="logout"),
    path('new/oauth/', views.new_oauth, name="new_oauth"),
]
