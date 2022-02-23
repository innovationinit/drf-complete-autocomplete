from collections import namedtuple


BaseAutocompleteModelDescription = namedtuple('AutocompleteModelDescription', [
    'api_name',
    'model',
    'value_field',
    'label_field',
    'icontains_search_fields',  # a list of searchable fields
    'filterset',
    'order_by',
    'distinct',
    'results_limit',
    'result_serializer',
])


class AutocompleteModelDescription(BaseAutocompleteModelDescription):
    @property
    def queryset(self):
        return self.model.objects.order_by(*self.order_by)


try:
    from django_filters.filterset import FilterSet


    def autocomplete_filterset_factory(filter_model, filters):
        class Meta:
            model = filter_model

        filterset_dict = {
            'Meta': Meta,
        }
        filterset_dict.update(filters)
        return type('AutocompleteFilterSet', (FilterSet,), filterset_dict)
except ImportError:
    pass
