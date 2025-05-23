from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.template.defaultfilters import title
from django.utils.http import urlencode
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
        context["search_form"] = GenreSearchForm(
            initial={"title": title}
        )

        titles_dict = {
            "book": reverse("media:book_list"),
            "film": reverse("media:film_list"),
            "comic": reverse("media:comic_list"),
            "series": reverse("media:series_list"),
            "anime": reverse("media:anime_list")
        }

        if "title" in self.request.GET and self.request.GET["title"] in titles_dict:
            title_name = self.request.GET["title"]
            self.request.session["genre_title"] = title_name
        elif "genre_title" in self.request.session.keys() and self.request.GET["title"] in titles_dict:
            title_name = self.request.session["genre_title"]
        else:
            title_name = "book"

        context["redirect_url"] = titles_dict[title_name]
        context["title"] = title_name
        return context
