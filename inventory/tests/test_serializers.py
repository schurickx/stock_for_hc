from inventory.models import Provider
from inventory.serializers import ProviderSerializer
from django.test import TestCase


class ProviderSerializerTestCase(TestCase):
    def test_ok(self):
        provider_1 = Provider.objects.create(title="Atlant")
        provider_2 = Provider.objects.create(title="Cooper")
        serializer_data = ProviderSerializer([provider_1, provider_2], many=True).data
        expected_data = [
            {
                'id': provider_1.id,
                'title': "Atlant"
            },
            {
                'id': provider_2.id,
                'title': "Cooper"
            },
        ]
        self.assertEqual(expected_data, serializer_data)