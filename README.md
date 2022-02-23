# DRF complete autocomplete

![Test package](https://github.com/innovationinit/drf-complete-autocomplete/actions/workflows/test-package.yml/badge.svg?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/innovationinit/drf-complete-autocomplete/badge.svg)](https://coveralls.io/github/innovationinit/drf-complete-autocomplete)

## Installation
```
$ pip install drf-complete-autocomplete
$ pip install drf-complete-autocomplete[django-filter]
```

## How to use

Settings:
```
from drf_complete_autocomplete.configuration import AutocompleteModelDescription

from my_app.models import MyModel


AUTOCOMPLETE_MODELS = [
    AutocompleteModelDescription(
        api_name='my_model',
        model=MyModel,
        value_field='pk',
        label_field='__unicode__',
        icontains_search_fields=['name'],
        filterset=None,  # django-filter FilterSet
        order_by=['name'],
        distinct=False,
        results_limit=20,
    ),
]
```

Serializer:
```
...
from drf_autocomplete.serializers import WithAutocomplete
...


class SomeModelSerializer(WithAutocomplete, serializers.ModelSerializer):
    ...

    class Meta:
        model = SomeModel
        fields = [
            ...
            'related_to_my_model',
            ...
        ]
        ...
        autocomplete_fields = {
            'related_to_my_model': 'my_model',
        }
```

View:

You can import `drf_complete_autocomplete.views.RetrieveAutocompleteResultsApiView` and supply your AUTOCOMPLETE_MODELS
 in urls file `RetrieveAutocompleteResultsApiView.as_view(autocomplete_config=AUTOCOMPLETE_MODELS)`.

Or use mixin `drf_complete_autocomplete.views.RetrieveAutocompleteResultsMixin` to create your own view.


## License
The DRF complete autocomplete package is licensed under the [FreeBSD
License](https://opensource.org/licenses/BSD-2-Clause).
