from django import forms
from django.utils.encoding import force_text

import django_filters

from .widgets import WithSquareBracketsHandlingWidget


class ListField(forms.Field):

    """Field for use in autocompletes filter sets only"""

    widget = WithSquareBracketsHandlingWidget
    default_error_messages = {
        'invalid_list': 'Enter a list of values.',
    }

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise forms.ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return [force_text(val) for val in value]

    def validate(self, value):
        if self.required and not value:
            raise forms.ValidationError(self.error_messages['required'], code='required')

    def has_changed(self, initial, data):
        if self.disabled:
            return False
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = set(force_text(value) for value in initial)
        data_set = set(force_text(value) for value in data)
        return data_set != initial_set


class ListFilter(django_filters.Filter):
    field_class = ListField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super(ListFilter, self).__init__(*args, **kwargs)
