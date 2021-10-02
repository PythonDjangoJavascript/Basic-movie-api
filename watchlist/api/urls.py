from django.urls import path
from watchlist.api import views


urlpatterns = [
    path("", views.WatchlistAPIView.as_view(), name="watch-list"),
    path("<int:pk>/", views.WatchDetailAPIView.as_view(), name="movie-detail"),
    path("stream-platforms/", views.StreamPlatformAPIView.as_view(),
         name="stream-platform"),
    # path("stream-platforms/<int:pk>/",
    #      views.StreamPlatformAPIView.as_view(), name="stream-detail"),
]
