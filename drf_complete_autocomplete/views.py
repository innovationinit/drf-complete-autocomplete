import six

from django.db.models import Q
from django.utils.functional import cached_property

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import autocomplete_result_serializer_factory


class RetrieveAutocompleteResultsMixin(object):

    serializer_class = None
    autocomplete_config = None

    def __init__(self, **kwargs):
        super(RetrieveAutocompleteResultsMixin, self).__init__(**kwargs)
        assert self.autocomplete_config is not None

    @cached_property
    def model_description(self):
        api_name = self.request.GET.get('model', '')
        return next(
            (description for description in self.autocomplete_config if description.api_name == api_name),
            None,
        )

    def retrieve(self, *args, **kwargs):
        serializer = self.get_serializer()
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        api_name = self.request.GET.get('model', '')
        search_term = self.request.GET.get('q', '')
        search_values = self.request.GET.getlist('values[]')
        exclude_values = filter(
            bool,
            self.request.GET.getlist('exclude', self.request.GET.getlist('exclude[]', [])),
        )
        if not self.model_description:
            raise NotFound('Autocomplete is unavailable for model {}.'.format(api_name))
        queryset = self.get_queryset(self.model_description, term=search_term, values=search_values, exclude=exclude_values)
        serializer_class = self.get_serializer_class()
        return serializer_class(queryset, many=True)

    def get_serializer_class(self):
        if self.serializer_class is not None:
            return self.serializer_class

        if self.model_description.result_serializer is None:
            return autocomplete_result_serializer_factory(
                self.model_description.value_field,
                self.model_description.label_field,
            )

        return self.model_description.result_serializer

    def get_queryset(self, description=None, term=None, values=None, exclude=None):
        if description is None:  # Browsable API uses get_queryset()
            return

        queryset = description.queryset

        # filter by values (no filtering propagation here)
        if values:
            return queryset.filter(**{'{}__in'.format(description.value_field): values})

        # filter by term
        if term:
            term_query = six.moves.reduce(
                lambda q, field_name: q | Q(**{'{}__icontains'.format(field_name): term}),
                description.icontains_search_fields,
                Q())
            queryset = queryset.filter(term_query)

        # exclude values
        if exclude:
            queryset = queryset.exclude(**{'{}__in'.format(description.value_field): exclude})

        # filter using a filterset
        if description.filterset:
            queryset = description.filterset(data=self.request.query_params, queryset=queryset).qs

        if description.distinct:
            queryset = queryset.distinct()

        return queryset[:description.results_limit]


class RetrieveAutocompleteResultsApiView(RetrieveAutocompleteResultsMixin, APIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
