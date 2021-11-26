import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.models import Provider
from inventory.serializers import ProviderSerializer


class ProviderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.provider1 = Provider.objects.create(title="Atlant")
        self.provider2 = Provider.objects.create(title="Cooper")

    def test_get(self):
        url = reverse('provider-list')
        self.client.force_login(self.user)
        response = self.client.get(url)
        serializer = ProviderSerializer(
            [self.provider1, self.provider2], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filter(self):
        url = reverse('provider-list')
        self.client.force_login(self.user)
        response = self.client.get(url, data={'title': 'Cooper'})
        serializer = ProviderSerializer([self.provider2], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        self.assertEqual(2, Provider.objects.count())
        url = reverse('provider-list')
        data = {'title': 'OOO "Perforator"'}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, Provider.objects.count())

    def test_update(self):
        url = reverse('provider-detail', args=(self.provider2.id,))
        data = {'title': 'OOO "MegaCOM"'}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.provider2 = Provider.objects.get(pk=self.provider2.id)
        self.provider2.refresh_from_db()
        self.assertEqual('OOO "MegaCOM"', self.provider2.title)
