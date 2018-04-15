"""Views of main page."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """Index page."""
    return render(request, "web/index.html", {
        "user": request.user,
    })
