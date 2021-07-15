from rest_framework import status
from rest_framework.test import APITestCase

from providers.tests import create_user
from providers.models import Provider

from .models import ServiceArea


class CreateServiceAreaTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.provider_data = {
            "name": "uber",
            "phone_number": "+23412345566",
            "language": "french",
            "currency": "USD"
        }
        self.provider = Provider.objects.create(user=self.user, **self.provider_data)
        self.service_area_data = {'name': 'Test', 'price': '10.5', 'provider': self.provider.id,
                                  'polygon': 'POLYGON ((-98.503358 29.335668, -98.503086 29.335668, -98.503086 '
                                             '29.335423, -98.503358 29.335423, -98.503358 29.335668))'}

    def test_can_create_area(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/service-areas/', self.service_area_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadServiceAreaTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.provider_data = {
            "name": "uber",
            "phone_number": "+23412345566",
            "language": "french",
            "currency": "USD"
        }
        self.provider = Provider.objects.create(user=self.user, **self.provider_data)
        self.service_area_data = {'name': 'Test', 'price': '10.5',
                                  'polygon': 'POLYGON ((-98.503358 29.335668, -98.503086 29.335668, -98.503086 '
                                             '29.335423, -98.503358 29.335423, -98.503358 29.335668))'}
        self.service_area = ServiceArea.objects.create(provider=self.provider, **self.service_area_data)

    def test_read_service_area_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/service-areas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_service_area_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/service-areas/' + str(self.service_area.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_find_correct_query(self):
        response = self.client.get(
            '/service-areas/get_areas/?long={}&lat={}'.format("-98.503358", "29.335668"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)
