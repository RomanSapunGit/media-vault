from media.forms.forms import (
    BookForm, FilmForm,
    GenreFilterForm, MediaSearchForm,
    SeriesForm, UserSearchForm
)
from media.models import Book, Film, Genre, Series
from media.utils import get_reverse_choice


class BookMutateMixin:
    model = Book
    template_name = "media/form/media-form.html"
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_type = get_reverse_choice(self.request.GET.get("type", None), Book.type)
        if not self.object:
            genre_ids = []
            if "genres" in self.request.GET:
                genre_ids = Genre.objects.filter(
                    name__in=self.request.GET.getlist("genres")
                ).values_list("id", flat=True)
            query_param_dict = {"type": db_type, "genres": genre_ids}

            context["form"] = BookForm(initial=query_param_dict)
        context["media_name"] = "book"
        context["params"] = self.request.GET.copy()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response


class FilmMutateMixin:
    model = Film
    template_name = "media/form/media-form.html"
    form_class = FilmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_ids = []
        if not self.object:
            if "genres" in self.request.GET:
                genre_ids = Genre.objects.filter(
                    name__in=self.request.GET.getlist("genres")
                ).values_list("id", flat=True)

            context["form"] = FilmForm(initial={"genres": genre_ids})
        context["media_name"] = "film"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response


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
        queryset = super().get_queryset()
        search_form = MediaSearchForm(self.request.GET)

        if search_form.is_valid():
            queryset = queryset.filter(
                title__icontains=search_form.cleaned_data["title"]
            )

        type_choice = self.request.GET.get("type")
        db_stored_choice = get_reverse_choice(type_choice, Book.type)
        if db_stored_choice:
            queryset = queryset.filter(
                type=db_stored_choice
            )

        genres_form = GenreFilterForm(self.request.GET)
        if genres_form.is_valid():
            queryset = queryset.filter(
                genres__name__in=genres_form.cleaned_data["genres"]
            )
        return queryset
