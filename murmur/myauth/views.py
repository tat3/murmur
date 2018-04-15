"""Authentication views."""

import os

from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import logout

from social_django.models import UserSocialAuth

from .models import UserRelation


def add_app_name(file_name):
    """Create path of HTML file."""
    return os.path.join("myauth", file_name)


def _oauth_login_required(user):
    """Decorator function to reject the user who do not login with OAuth."""
    if user.is_anonymous:
        return False
    try:
        UserSocialAuth.objects.get(user=user)
    except:
        return False
    return True


oauth_login_required = user_passes_test(_oauth_login_required)


# @login_required
# def index(request):
#     """Index page."""
#     return render(request, add_app_name('index.html'))


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
            # Save new user and relation between it and access_token
            form.save()
            owner = UserSocialAuth.objects.get(user=request.user)
            user = User.objects.get(username=request.POST.get("username"))
            relation = UserRelation(owner=owner, user=user)
            relation.save()
            return HttpResponseRedirect(reverse('myauth:login'))
        return render(request, add_app_name('new.html'), {'form': form, })
    else:
        raise Http404


def new_oauth(request):
    """Oauth sing-up page."""
    logout(request)
    return render(request, add_app_name('new_oauth.html'))
