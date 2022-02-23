from rest_framework import serializers

from drf_complete_autocomplete.serializers import WithAutocomplete

from .models import Address


class AddressSerializer(WithAutocomplete, serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            'region',
            'country',
            'post',
        )
        autocomplete_fields = {
            'region': 'region',
            'country': 'country',
            'post': 'post',
        }
        autocomplete_field_dependencies = {
            'region.country': 'country',
            'post.region': 'region',
        }
        autocomplete_filters = {
            'country': {
                'is_fairy': True,
            }
        }
