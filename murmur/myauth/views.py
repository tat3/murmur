"""Authentication views."""

import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from social_django.models import UserSocialAuth

from .models import UserRelation


def add_app_name(file_name):
    """Create path of HTML file."""
    return os.path.join("myauth", file_name)


def oauth_login_required(user):
    """Decorator function to reject the user who do not login with OAuth."""
    if user.is_anonymous():
        return False
    try:
        user_qs = UserSocialAuth.objects.get(user=user)
    except:
        return False
    return True


oauth_login_required = user_passes_test(oauth_login_required)


@login_required
def index(request):
    """Index page."""
    return render(request, add_app_name('index.html'))


@oauth_login_required
def new(request):
    """Send user creation form."""
    form = UserCreationForm()
    return render(request, add_app_name('new.html'), {'form': form, })


@oauth_login_required
def create(request):
    """Create new user using post data."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            owner = UserSocialAuth.objects.get(user=request.user)
            relation = UserRelation(owner=owner, user=form)
            return HttpResponseRedirect(reverse('myauth:login'))
        return render(request, add_app_name('new.html'), {'form': form, })
    else:
        raise Http404


def new_oauth(request):
    """Oauth sing-up page."""
    form = UserCreationForm()
    return render(request, add_app_name('new_oauth.html'), {'form': form, })
