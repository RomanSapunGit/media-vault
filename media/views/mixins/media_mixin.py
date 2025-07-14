from django.db.models import Count, Q, Avg
from django.urls import reverse_lazy

from media.forms.filter_forms import CreatorFilterForm, GenreFilterForm
from media.forms.forms import CreatorForm
from media.forms.media_forms import BookForm, FilmForm, SeriesForm
from media.models import Series, Film, Book, Creator, Genre
from media.utils import get_reverse_choice


class MediaMutateMixin:
    def form_valid(self, form):
        if not self.object:
            form.instance.created_by = self.request.user.username
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["creator_form"] = CreatorForm()
        return context

    def get_initial(self):
        initial = super().get_initial()
        genre_names = self.request.GET.getlist("genres")
        if self.request.method == "GET" and genre_names:
            genre_ids = Genre.objects.filter(
                name__in=genre_names
            ).values_list("id", flat=True)
            initial["genres"] = genre_ids

        creator_names = self.request.GET.getlist("creators")
        if self.request.method == "GET" and creator_names:
            genre_ids = Creator.objects.filter(
                first_name__in=creator_names
            ).values_list("id", flat=True)
            initial["creators"] = genre_ids

        return initial


class BookMutateMixin(MediaMutateMixin):
    model = Book
    form_class = BookForm
    template_name = "media/form/book_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "book"
        context["params"] = self.request.GET.copy()
        return context

    def get_initial(self):
        initial = super().get_initial()

        if self.request.method == "GET" and "type" in self.request.GET:
            type_value = self.request.GET.get("type")
            initial["type"] = get_reverse_choice(type_value, Book.type)

        return initial


class FilmMutateMixin(MediaMutateMixin):
    model = Film
    form_class = FilmForm
    template_name = "media/form/film_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "film"
        return context


class SeriesMutateMixin(MediaMutateMixin):
    model = Series
    form_class = SeriesForm
    template_name = "media/form/series_form.html"

    def get_initial(self):
        initial = super().get_initial()

        if self.request.method == "GET":
            if "type" in self.request.GET:
                type_value = self.request.GET.get("type")
                initial["type"] = get_reverse_choice(type_value, Series.type)
            if "status" in self.request.GET:
                status_value = self.request.GET.get("status")
                initial["status"] = get_reverse_choice(
                    status_value, Series.status
                )

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "series"
        return context


class MediaListMixin:
    url_create = None

    def get_filter_forms(self, query_params=None):
        if not hasattr(self, "_filter_forms"):
            self._filter_forms = {
                "genre_filter_form":
                    GenreFilterForm(query_params) if "genres" in query_params else GenreFilterForm(),
                "creators_filter_form":
                    CreatorFilterForm(query_params) if "creators" in query_params else CreatorFilterForm(),
            }
        return self._filter_forms

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .prefetch_related("genres", "creators", "media_ratings")
            .annotate(
                reviews_num=Count(
                    "media_ratings",
                    filter=Q(media_ratings__is_hidden=False)
                ),
                reviews_avg=Avg(
                    "media_ratings__rating",
                    filter=Q(
                        media_ratings__is_hidden=False,
                        media_ratings__rating__isnull=False
                    )
                )
            )
        )

        forms = self.get_filter_forms(self.request.GET)
        if forms["genre_filter_form"].is_valid():
            queryset = queryset.filter(
                genres__name__in=forms["genre_filter_form"]
                .cleaned_data["genres"]
            )

        if forms["creators_filter_form"].is_valid():
            queryset = queryset.filter(
                creators__first_name__in=forms["creators_filter_form"]
                .cleaned_data["creators"]
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        if not context.get("query_params"):
            context["query_params"] = self.request.GET.copy()
        context["url_create"] = self.url_create
        forms = self.get_filter_forms(context["query_params"])
        context["genre_filter_form"] = forms["genre_filter_form"]
        context["creators_filter_form"] = forms["creators_filter_form"]

        return context


class MediaNameSessionMixin:
    media_name = None
    redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        media_dict = {
            "book": reverse_lazy("media:book_list"),
            "film": reverse_lazy("media:film_list"),
            "comic": f"{reverse_lazy('media:book_list')}?type=comic",
            "series": reverse_lazy("media:series_list"),
            "anime": f"{reverse_lazy('media:series_list')}?type=Anime"
        }

        if "media" in request.GET:
            media_query = request.GET["media"]
            media_name = media_query if media_query in media_dict else "book"
            request.session["media_chosen"] = media_name
        elif "media_chosen" in request.session:
            media_name = request.session["media_chosen"]
        else:
            media_name = "book"

        self.media_name = media_name
        self.redirect_url = media_dict[media_name]

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["media"] = self.media_name
        context["redirect_url"] = self.redirect_url
        return context


class MediaTypeCountMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        media_chosen = self.request.session.get("media_chosen", "book")
        media_type_to_filter = {
            "book": Count("media__book"),
            "film": Count("media__film"),
            "series": Count("media__series"),
            "comic": (Count(
                "media__book",
                filter=Q(media__book__type="CS"))
            ),
            "anime": (Count(
                "media__series",
                filter=Q(media__series__type="AE"))
            )
        }
        return queryset.annotate(
            media_type_count=media_type_to_filter[media_chosen]
        )


class MediaTypeFilterMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        media_chosen = self.request.session.get("media_chosen", "book")
        media_type_to_filter = {
            "book": {"media__book__isnull": False},
            "film": {"media__film__isnull": False},
            "series": {"media__series__isnull": False},
            "comic": {"media__book__isnull": False,
                      "media__book__type": "CS"},
            "anime": {"media__series__isnull": False,
                      "media__series__type": "AE"}
        }
        return queryset.filter(**media_type_to_filter[media_chosen])
