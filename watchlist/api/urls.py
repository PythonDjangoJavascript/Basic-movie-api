from django.urls import path
from django.urls.conf import include
from watchlist.api import views
from rest_framework.routers import DefaultRouter


# Initialize Default router for viewsets
router = DefaultRouter()
router.register('streams', views.StreamPlatformViewSets, basename="stream")


urlpatterns = [
    path("watchlist/", views.WatchlistAPIView.as_view(), name="watch-list"),
    path("watchlist/<int:pk>/",
         views.WatchDetailAPIView.as_view(), name="movie-detail"),
    path("stream-platforms/", views.StreamPlatformAPIView.as_view(),
         name="stream-platform"),
    path("stream-platforms/<int:pk>/",
         views.StreamPlatformDetialAPIView.as_view(), name="stream-detail"),
    path('', include(router.urls)),
    path("watchlist/<int:pk>/reviews/",
         views.ReviewListAPIView.as_view(), name="movie-reviews"),
    path('watchlist-filter/', views.WatchListFilterAPIView.as_view(),
         name="watchlist-filter"),
    #     path("reviews/", views.ReviewListAPIView.as_view(), name="reviews"),
    path("reviews/<int:pk>/", views.ReviewDetailAPIView.as_view(),
         name="review-detail"),
    path("user-reviews/", views.UserReview.as_view(), name="user-review"),
]
