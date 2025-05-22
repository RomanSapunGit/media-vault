from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    media_users_count = get_user_model().objects.count()
    context = {
        "media_users_count": media_users_count
    }
    return render(request, "home/index.html", context)
