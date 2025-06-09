from media.forms import BookForm
from media.models import Book


class BookMutateMixin:
    model = Book
    template_name = "media/form/media-form.html"
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_type = get_reverse_choice(self.request.GET.get("type", None), Book.type)
        genre_ids = []
        if "genres" in self.request.GET:
            genre_ids = Genre.objects.filter(
                name__in=self.request.GET.getlist("genres")
            ).values_list("id", flat=True)
        query_param_dict = {"type": db_type, "genres": genre_ids}

        context["media_name"] = "book"
        return context

    def form_valid(self, form):
        self.object.users.add(self.request.user)
        return response


class FilmMutateMixin:
    model = Film
    template_name = "media/form/media-form.html"
    form_class = FilmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_ids = []
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



