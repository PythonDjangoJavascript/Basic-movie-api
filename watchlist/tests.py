from django.contrib.auth import get_user_model
from django.urls.base import reverse
# from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from watchlist.models import StreamPlatform, WatchList, Review
from watchlist.api.serializers import ReviewSerializer, StreamPlatformSerializer


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
        user = get_user_model().objects.create_superuser(**default)
    else:
        user = get_user_model().objects.create_user(**default)

    return {
        "token": Token.objects.get(user__username=default["username"]),
        "user": user
    }


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
        self.token = create_user().get("token")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.platform = sample_movie_platform()

    def test_platform_creat_success(self):
        """Test Admin user can create new platform"""

        # create admin user and get token
        admin_token = create_user(
            username="Admin",
            is_staff=True,
            is_superuser=True
        ).get("token")
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

    def setUp(self) -> None:
        self.client = APIClient()

        user_info = create_user()
        self.user = user_info.get("user")
        self.token = user_info.get("token")

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.platform = sample_movie_platform()
        self.movie = create_movie(self.platform)
        self.review = create_review(self.user, self.movie)

    def test_get_moview_reviews_list_workd(self):
        """Test Get review list for perticular review works"""

        response = self.client.get(
            reverse('movie-reviews', args=(self.movie.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_reivews = ReviewSerializer(response.data, many=True)
        self.assertEqual(response.data, serialized_reivews.data)

    def test_reivew_create(self):
        """Test user can create review"""

        # creating new movie as logged user has already reviewed self.movie
        new_movie = create_movie(self.platform)

        payload = {
            "rating": 4,
            "message": "Test Review Two"
        }

        response = self.client.post(
            reverse("movie-reviews", args=(new_movie.id,)), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
