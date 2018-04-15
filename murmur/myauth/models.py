"""Models for usual authentication."""

from django.db import models
from django.contrib.auth.models import User


class UserRelation(models.Model):
    """Associate user account and OAuth keys."""

    owner = models.ForeignKey('social_django.UserSocialAuth',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True)
