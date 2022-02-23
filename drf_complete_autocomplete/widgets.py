from django.forms.widgets import (
    SelectMultiple,
    Widget,
)
from django.utils.datastructures import MultiValueDict


class WithSquareBracketsHandlingWidget(Widget):
    """Widget getting value from data dict for name and name[]"""

    def value_from_datadict(self, data, files, name):
        """Try to get value from name key, if it fails try name[]."""
        if isinstance(data, MultiValueDict):
            return data.getlist(name, data.getlist(u'{field_name}[]'.format(field_name=name)))
        return data.get(name)


class WithSquareBracketsHandlingSelectMultiple(WithSquareBracketsHandlingWidget, SelectMultiple):
    """SelectMultiple widget with fallback for getting list not only for field name but also name[]."""
