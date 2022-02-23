import six

from rest_framework import fields
from rest_framework.serializers import Serializer


def autocomplete_result_serializer_factory(value_field, label_field):
    class AutocompleteResultSerializer(Serializer):
        value = fields.CharField(source=value_field)
        label = fields.CharField(source=label_field)

    return AutocompleteResultSerializer


def autocomplete_results_serializer_factory(result_serializer_class):
    class AutocompleteResultsSerializer(Serializer):
        results = result_serializer_class(many=True)

    return AutocompleteResultsSerializer


class WithAutocomplete(object):

    def __init__(self, *args, **kwargs):
        super(WithAutocomplete, self).__init__(*args, **kwargs)

        autocomplete_fields = getattr(self.Meta, 'autocomplete_fields', None)
        if not autocomplete_fields:
            return

        for field_name, model_api_name in six.iteritems(autocomplete_fields):
            if field_name in self.fields:
                self.fields[field_name].is_autocomplete = True
                self.fields[field_name].model_api_name = model_api_name

        autocomplete_field_dependencies = getattr(self.Meta, 'autocomplete_field_dependencies', {})

        for filter_target, filter_source in six.iteritems(autocomplete_field_dependencies):
            field_name, filter_field = filter_target.split('.', 1)
            if field_name in self.fields:
                if not hasattr(self.fields[field_name], 'autocomplete_dependencies'):
                    self.fields[field_name].autocomplete_dependencies = {}
                self.fields[field_name].autocomplete_dependencies[filter_field] = filter_source

        autocomplete_filters = getattr(self.Meta, 'autocomplete_filters', {})

        for field_name, filters in six.iteritems(autocomplete_filters):
            self.fields[field_name].autocomplete_filters = filters
