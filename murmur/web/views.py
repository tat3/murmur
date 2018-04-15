"""Views of main page."""

import json

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse

from social_django.models import UserSocialAuth

from murmur.myauth.models import UserRelation
from .utils import TwitterClient


def _usual_login_required(user):
    """Decorator function to reject OAuth-login user."""
    if user.is_anonymous:
        return False
    try:
        UserSocialAuth.objects.get(user=user)
    except:
        return True
    return False


usual_login_required = user_passes_test(_usual_login_required)


@usual_login_required
def index(request):
    """Index page."""
    return render(request, "web/index.html", {
        "results": json.load(open("murmur/web/json/result.json", "r"))
    })


@usual_login_required
def test(request):
    """Test page."""
    user = request.user
    owner = UserRelation.objects.get(user=user).owner
    return render(request, "web/test.html", {
        "user": user,
        "owner": owner.access_token["oauth_token"]
    })


@usual_login_required
def update(request):
    """Update status using POST data."""
    if "text" not in request.POST:
        return HttpResponseRedirect(reverse("web:index"))
    text = request.POST.get("text")
    user = request.user
    owner = UserRelation.objects.get(user=user).owner

    twitter = TwitterClient(user_social=owner)

    try:
        twitter.status_update(text)
    except:
        return HttpResponseRedirect(reverse("web:error"))

    return HttpResponseRedirect(reverse("web:index"))
