from drf_complete_autocomplete.configuration import AutocompleteModelDescription
from drf_complete_autocomplete.serializers import autocomplete_result_serializer_factory

from .models import (
    Country,
    Post,
    Region,
)


AUTOCOMPLETE_MODELS = [
    AutocompleteModelDescription(
        api_name='region',
        model=Region,
        value_field='id',
        label_field='get_name',
        icontains_search_fields=['name'],
        filterset=None,
        order_by=['name'],
        distinct=False,
        results_limit=10,
        result_serializer=None,
    ),
    AutocompleteModelDescription(
        api_name='country',
        model=Country,
        value_field='id',
        label_field='name',
        icontains_search_fields=['name'],
        filterset=None,
        order_by=['name'],
        distinct=False,
        results_limit=10,
        result_serializer=None,
    ),
    AutocompleteModelDescription(
        api_name='post',
        model=Post,
        value_field='id',
        label_field='name',
        icontains_search_fields=['name'],
        filterset=None,
        order_by=['name'],
        distinct=False,
        results_limit=10,
        result_serializer=autocomplete_result_serializer_factory('zip_code', 'name'),
    )
]
