from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient


# All Static Variables
REGISTRATION_URL = reverse('user:register')
LOGIN_URL = reverse('user:login')


def create_user(**params):
    """Create test user"""

    return get_user_model().objects.create_user(**params)


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
        user = get_user_model().objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_duplicate_user(self):
        """Test if duplicate user can be created or not"""

        payload = {
            "username": "test",
            "email": "test@email.com",
            "password": "123",
            "password2": "123"
        }
        payload2 = {
            "username": "test",
            "email": "test@email.com",
            "password": "123"
        }

        create_user(**payload2)
        total_user = get_user_model().objects.all().count()
        self.assertEqual(1, total_user)

        response = self.client.post(REGISTRATION_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_token_is_created(self,):
        """Test Valid token is generated in login and registration"""

        payload = {
            "username": "test",
            "email": "test@email.com",
            "password": "123",
            "password2": "123"
        }
        response = self.client.post(REGISTRATION_URL, payload)

        self.assertIn("Token", response.data)

    def test_login(self):
        """Test login returns token"""
        payload = {
            "username": "test login",
            "password": "superSecretPassword123"
        }

        create_user(**payload)

        user = get_user_model().objects.get(pk=1)
        self.assertEqual("test login", user.username)

        self.assertTrue(user.check_password(payload["password"]))
        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_token_genaration_for_invalid_user(self):
        """Test token invalit user token genaration"""

        payload = {
            "username": "invalid user",
            "password": "123"
        }
        response = self.client.post(LOGIN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_genaration_with_wrong_credintials(self):
        payload = {
            "username": "test",
            "password": "123"
        }
        wrong_payload = {
            "username": "test",
            "password": "wrongpassword"
        }
        invalid_payload = {
            "username": "test",
            "password": ""
        }
        response = self.client.post(LOGIN_URL, wrong_payload)
        response2 = self.client.post(LOGIN_URL, invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
