from django.urls import path
from watchlist.api import views


urlpatterns = [
    path("watchlist/", views.WatchlistAPIView.as_view(), name="watch-list"),
    path("watchlist/<int:pk>/",
         views.WatchDetailAPIView.as_view(), name="movie-detail"),
    path("stream-platforms/", views.StreamPlatformAPIView.as_view(),
         name="stream-platform"),
    path("stream-platforms/<int:pk>/",
         views.StreamPlatformDetialAPIView.as_view(), name="stream-detail"),
    path("watchlist/<int:pk>/reviews/",
         views.ReviewListAPIView.as_view(), name="movie-reviews"),
    #     path("reviews/", views.ReviewListAPIView.as_view(), name="reviews"),
    path("reviews/<int:pk>/", views.ReviewDetailAPIView.as_view(),
         name="review-detail"),
]
