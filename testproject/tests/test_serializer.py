from django.test import TestCase

from testapp.serializers import AddressSerializer


class SerializerWithAutocompleteTestCase(TestCase):

    def test_setting_meta_data_on_fields(self):
        serializer = AddressSerializer()

        # Fields not specified in config are not touched
        self.assertFalse(
            hasattr(serializer.fields['id'], 'is_autocomplete')
        )

        # Fields specified as autocomplete are marked
        self.assertTrue(serializer.fields['region'].is_autocomplete)
        self.assertEqual(serializer.fields['region'].model_api_name, 'region')

        self.assertTrue(serializer.fields['country'].is_autocomplete)
        self.assertEqual(serializer.fields['country'].model_api_name, 'country')

        # Fields with dependencies in autocomplete are marked properly
        self.assertDictEqual(serializer.fields['region'].autocomplete_dependencies, {
            'country': 'country',
        })

        # Fields with defined standard filters to use in autocomplete
        self.assertDictEqual(serializer.fields['country'].autocomplete_filters, {
            'is_fairy': True,
        })
