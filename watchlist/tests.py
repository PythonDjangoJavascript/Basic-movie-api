from django.contrib.auth import get_user_model
from django.urls.base import reverse
# from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from watchlist.models import StreamPlatform, WatchList, Review
from watchlist.api.serializers import StreamPlatformSerializer


# All Endpoints
STREAM_PLATFORM = reverse('stream-platform')


def create_user(**params):
    """Create user and returns the user token"""
    default = {
        "username": "Sample Test User",
        "email": "defaulttest@user.com",
        "password": "SuperSecreatPassword"
    }
    # if params provided
    default.update(params)

    # if user is super user
    if params.get("is_superuser"):
        get_user_model().objects.create_superuser(**default)
    else:
        get_user_model().objects.create_user(**default)

    return Token.objects.get(user__username=default["username"])


def sample_movie_platform(**params):
    """Create and returns a new movie platform"""

    default = {
        "name": "Netflix",
        "about": "Movie Washing site",
        "website": "https://netflix.com/"
    }

    # update default if an params provided
    default.update(params)
    # now create a new platform
    return StreamPlatform.objects.create(**default)


def create_movie(platform, **params):
    """Add a new movie in watchlist database"""

    default = {
        "platform": platform,
        "title": "The Test Movie",
        "storyline": "The quick brown fox jumps over the lazy dog"
    }
    default.update(params)
    return WatchList.objects.create(**default)


def create_review(reviewer, movie, **params):
    """Create a new review to an individual movie"""

    default = {
        "review_user": reviewer,
        "watchlist": movie,
        "rating": 5,
        "message": "Test Review"
    }
    default.update(params)
    return Review.objects.create(**default)


class StearmPlatformTests(APITestCase):
    """Tests Stream Platform api endpoints"""

    def setUp(self) -> None:
        self.client = APIClient()

        # create a user and set the user token in the header section
        self.token = create_user()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.platform = sample_movie_platform()

    def test_platform_creat_success(self):
        """Test Admin user can create new platform"""

        # create admin user and get token
        admin_token = create_user(
            username="Admin",
            is_staff=True,
            is_superuser=True
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)

        payload = {
            "name": "Amazon Prime",
            "about": "Movie Hosting site",
            "website": "https://amazoneprimce.com/"
        }

        response = self.client.post(STREAM_PLATFORM, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        all_platform = StreamPlatform.objects.all()
        serialized_platforms = StreamPlatformSerializer(
            all_platform, many=True)
        self.assertIn(response.data, serialized_platforms.data)

    def test_normal_user_cant_create_platform(self):
        payload = {
            "name": "Amazon Prime",
            "about": "Movie Hosting site",
            "website": "https://amazoneprimce.com/"
        }

        response = self.client.post(STREAM_PLATFORM, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list_endpont(self):
        """Test normal user can access all streaming platforms"""

        response = self.client.get(STREAM_PLATFORM)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_detail_get(self):
        """Test Platform detila retrieve endpoint wroks"""

        response = self.client.get(
            reverse('stream-detail', args=(self.platform.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StreamPlatform.objects.all().count(), 1)
        self.assertEqual(StreamPlatform.objects.get().name, self.platform.name)


# NOT TESTING WATCHLIST API END POINTS AS ALL TESTS WILL BE SAME TO PLATFORM


class ReviewTests(APITestCase):
    """Test Review Endpoints"""
    pass
