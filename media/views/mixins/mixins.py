from media.utils import get_reverse_choice


class SearchMixin:
    search_form = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        query_params = self.request.GET.copy()
        context["query_params"] = query_params
        context["search_form"] = self.search_form(query_params)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        form = self.search_form(self.request.GET)
        field_name = list(form.fields.keys())[0]
        if form and form.is_valid() and form.cleaned_data[field_name]:
            queryset = queryset.filter(
                **{f"{field_name}__icontains": form.cleaned_data[field_name]}
            )
        return queryset


class TypeChoiceMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["type_choices"] = [
            choice_type[1]
            for choice_type in self.model.type.field.choices
        ]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        type_choice = self.request.GET.get("type")
        db_stored_choice = get_reverse_choice(type_choice, self.model.type)
        if db_stored_choice:
            queryset = queryset.filter(
                type=db_stored_choice
            )
        return queryset
