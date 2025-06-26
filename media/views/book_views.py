from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from media.forms.search_forms import MediaSearchForm
from media.models import Book
from media.views.mixins.media_mixin import BookMutateMixin, MediaListMixin
from media.views.mixins.mixins import (
    SearchMixin,
    TypeChoiceMixin,
)


class BookListView(
    LoginRequiredMixin,
    MediaListMixin,
    SearchMixin,
    TypeChoiceMixin,
    generic.ListView
):
    model = Book
    paginate_by = 10
    template_name = "media/list/book_list.html"
    search_form = MediaSearchForm


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "media/detail/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "book"
        context["delete_url"] = reverse_lazy(
            "media:book_delete",
            args=[context["book"].id]
        )
        return context


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    success_url = reverse_lazy("media:book_list")


class BookCreateView(
    LoginRequiredMixin, BookMutateMixin,
    generic.CreateView
):
    success_url = reverse_lazy("media:book_list")
    navigate_url = reverse_lazy("media:creator_create")


class BookUpdateView(LoginRequiredMixin, BookMutateMixin, generic.UpdateView):
    def get_success_url(self):
        self.success_url = reverse_lazy(
            "media:book_detail", kwargs={"pk": self.object.id}
        )
        return super().get_success_url()
