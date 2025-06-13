from media.forms.forms import (
    BookForm, FilmForm,
    GenreFilterForm, MediaSearchForm,
    SeriesForm, UserSearchForm
)
from media.models import Book, Film, Genre, Series
from media.utils import get_reverse_choice


class MediaMutateMixin:
    template_name = "media/form/media-form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response

    def get_initial(self):
        initial = super().get_initial()
        genre_names = self.request.GET.getlist("genres")
        if self.request.method == "GET" and genre_names:
            genre_ids = Genre.objects.filter(
                name__in=genre_names
            ).values_list("id", flat=True)
            initial["genres"] = genre_ids

        return initial


class BookMutateMixin(MediaMutateMixin):
    model = Book
    form_class = BookForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "film"
        return context


class SeriesMutateMixin(MediaMutateMixin):
    model = Series
    form_class = SeriesForm

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
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["query_params"] = self.request.GET.copy()
        if "genres" in self.request.GET:
            context["genre_filter_form"] = GenreFilterForm(self.request.GET)
        else:
            context["genre_filter_form"] = GenreFilterForm()
        context["search_form"] = MediaSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = (super()
                    .get_queryset()
                    .prefetch_related("genres", "creators")
                    )

        search_form = UserSearchForm(self.request.GET)
        if search_form.is_valid():
            queryset = queryset.filter(
                title__icontains=search_form.cleaned_data["title"]
            )

        genres_form = GenreFilterForm(self.request.GET)
        if genres_form.is_valid():
            queryset = queryset.filter(
                genres__name__in=genres_form.cleaned_data["genres"]
            )
        return queryset
