from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Provider


def create_user():
    user_data = {
        'email': 'samuel@gmail.com',
        'password': 'password'
    }

    user = User.objects.create_user(**user_data)
    return user


class ProviderTest(APITestCase):

    def setUp(self):
        self.data = {
            "email": "user@example.com",
            "password": "testpassword",
            "provider": {
                "name": "uber",
                "phone_number": "+23412345534",
                "language": "french",
                "currency": "USD"
            }
        }
        self.provider_data = {
            "name": "uber",
            "phone_number": "+23412345566",
            "language": "french",
            "currency": "USD"
        }
        self.user = create_user()
        self.provider = Provider.objects.create(user=self.user, **self.provider_data)
        self.data.update({'language': "igbo"})

    def test_create_provider(self):
        response = self.client.post('/providers/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_providers(self):
        response = self.client.get("/providers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_provider(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/providers/' + str(self.provider.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/providers/' + str(self.provider.id) + "/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_delete_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/providers/' + str(self.provider.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
