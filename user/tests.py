from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


# All Static Variables
REGISTRATION_URL = reverse('user:register')


class PublicUserAPITests(APITestCase):
    """Tests all public user api endpoints"""

    def setUp(self) -> None:
        """Setup method will be available to every test method of this cls"""
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test User creation with valid payload works"""

        payload = {
            "username": "test",
            "email": "test@email.com",
            "password": "123",
            "password2": "123"
        }

        response = self.client.post(REGISTRATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
