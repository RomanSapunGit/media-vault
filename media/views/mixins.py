from media.forms import BookForm
from media.models import Book


class BookMutateMixin:
    model = Book
    template_name = "media/form/media-form.html"
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_name"] = "book"
        return context

    def form_valid(self, form):
        self.object.users.add(self.request.user)
        return super().form_valid(form)
