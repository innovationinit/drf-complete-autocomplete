import six

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from drf_complete_autocomplete.serializers import autocomplete_result_serializer_factory

from testapp import (
    autocomplete_settings,
    models,
)


class AutocompletesApiTestCase(TestCase):

    def test_getting_autocomplete_results(self):

        country = models.Country.objects.create(name='Neverland')
        region = models.Region.objects.create(name='Pirates Bay', country=country)
        post = models.Post.objects.create(name='Tortuga', zip_code='PB-TOR', region=region)

        data = {
            'region': [
                region,
            ],
            'country': [
                country,
            ],
            'post': [
                post,
            ]
        }
        for autocomplete_description in autocomplete_settings.AUTOCOMPLETE_MODELS:
            self._check_autocomplete_with_no_term(autocomplete_description, data)

    def _check_autocomplete_with_no_term(self, description, data):
        url = '{url}?model={model}'.format(url=reverse('autocompletes'), model=description.api_name)
        response = self.client.get(url, format='json')

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg='Autocomplete for {} returned bad status_code {} but expected {}'.format(
                description.api_name, response.status_code, status.HTTP_200_OK))

        self.assertIn(description.api_name, data)
        model_instances = data[description.api_name]

        item_count = len(response.data)
        expected_item_count = len(description.model.objects.all()[:description.results_limit])
        self.assertEqual(
            expected_item_count, len(model_instances),
            msg='Test for autocomplete for {} should expect {} items but found {}'.format(
                description.api_name, expected_item_count, len(model_instances)))
        self.assertEqual(
            item_count, expected_item_count,
            msg='Autocomplete for {} returned bad item count {} but expected {}'.format(
                description.api_name, item_count, expected_item_count))

        for model_instance in model_instances:
            serialized_instance = self._get_serializer(description)(model_instance).data
            api_result = next((result for result in response.data if serialized_instance['value'] == result['value']), None)
            self.assertIsNotNone(
                api_result, msg='No {} autocomplete result found for {}'.format(description.api_name, serialized_instance['value']))
            self.assertDictEqual(api_result, {
                'label': six.text_type(serialized_instance['label']),
                'value': serialized_instance['value'],
            })

    def _get_serializer(self, description):
        if description.result_serializer is None:
            return autocomplete_result_serializer_factory(
                description.value_field,
                description.label_field,
            )

        return description.result_serializer
