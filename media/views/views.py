from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from media.forms.forms import CreatorForm
from media.forms.search_forms import GenreSearchForm, CreatorSearchForm
from media.models import Genre, Media, Creator, UserMediaRating
from media.views.mixins.media_mixin import (
    MediaNameSessionMixin,
    MediaTypeCountMixin
)
from media.views.mixins.mixins import (
    SearchMixin
)


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    media_users_count = get_user_model().objects.count()
    context = {
        "media_users_count": media_users_count,
        "media_titles_count": Media.objects.all().count(),
        "media_ratings_count": UserMediaRating.objects.all().count()
    }
    return render(request, "home/index.html", context)


class GenreListView(
    LoginRequiredMixin,
    SearchMixin,
    MediaNameSessionMixin,
    MediaTypeCountMixin,
    generic.ListView
):
    model = Genre
    template_name = "media/list/genre_list.html"
    paginate_by = 10
    search_form = GenreSearchForm


class CreatorListView(
    LoginRequiredMixin,
    MediaNameSessionMixin,
    SearchMixin,
    MediaTypeCountMixin,
    generic.ListView
):
    model = Creator
    template_name = "media/list/creator_list.html"
    paginate_by = 10
    search_form = CreatorSearchForm



