"""Admin page."""

from django.contrib import admin

from .models import UserRelation

admin.site.register(UserRelation)
