"""Admin page."""

from django.contrib import admin

from .models import UserRelation


class UserRelationAdmin(admin.ModelAdmin):
    """Customize UserRelation's admin page."""

    list_display = ("owner", "user")

admin.site.register(UserRelation, UserRelationAdmin)
