from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from media.forms import GenreSearchForm
from media.models import Genre


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    media_users_count = get_user_model().objects.count()
    context = {
        "media_users_count": media_users_count
    }
    return render(request, "home/index.html", context)

class GenreListView(generic.ListView):
    model = Genre
    template_name = "media/genre_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["search_form"] = GenreSearchForm(self.request.GET)

        media_dict = {
            "book": reverse("media:book_list"),
            "film": reverse("media:film_list"),
            "comic": reverse("media:comic_list"),
            "series": reverse("media:series_list"),
            "anime": reverse("media:anime_list")
        }

        if "media" in self.request.GET:
            media_query = self.request.GET["media"]
            media_name = media_query if media_query in media_dict else "book"
            self.request.session["genre_media"] = media_name
        elif "genre_media" in self.request.session.keys():
            media_name = self.request.session["genre_media"]
        else:
            media_name = "book"

        context["redirect_url"] = media_dict[media_name]
        context["media"] = media_name
        return context

    def get_queryset(self):
        queryset = Genre.objects.all()
        form = GenreSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset