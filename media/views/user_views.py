from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic

from media.forms.search_forms import UserSearchForm
from media.forms.user_forms import MediaUserUpdateForm
from media.models import MediaUser, UserMediaRating


class UserListView(LoginRequiredMixin, generic.ListView):
    model = MediaUser
    paginate_by = 10
    template_name = "media/list/user_list.html"
    context_object_name = "user_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["query_params"] = self.request.GET.copy()
        context["search_form"] = UserSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = UserSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data["username"]:
            queryset = queryset.filter(
                username__icontains=search_form.cleaned_data["username"]
            )
        return queryset


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = MediaUser
    template_name = "media/detail/user_detail.html"
    context_object_name = "media_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = "user"
        context["delete_url"] = reverse_lazy(
            "media:user_delete",
            args=[context["media_user"].id]
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.id == self.kwargs["pk"]:
            queryset = queryset.prefetch_related(
                "media_ratings",
                "media_ratings__media"
            )
        else:
            filter_queryset = UserMediaRating.objects.filter(is_hidden=False)
            queryset = queryset.prefetch_related(Prefetch(
                "media_ratings", queryset=filter_queryset),
                Prefetch("media_ratings__media")
            )
        return queryset


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MediaUser
    success_url = reverse_lazy("media:user_list")


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = MediaUser
    template_name = "media/form/form.html"
    form_class = MediaUserUpdateForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def get_success_url(self):
        logout(self.request)
        return reverse_lazy("authentication:login")
