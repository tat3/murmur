"""Authentication views."""

import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def add_app_name(file_name):
    """Create path of HTML file."""
    return os.path.join("myauth", file_name)


@login_required
def index(request):
    """Index page."""
    return render(request, add_app_name('index.html'))


def new(request):
    """Send user creation form."""
    form = UserCreationForm()
    return render(request, add_app_name('new.html'), {'form': form, })


def create(request):
    """Create new user using post data."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myauth:login'))
        return render(request, add_app_name('new.html'), {'form': form, })
    else:
        raise Http404
