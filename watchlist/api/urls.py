from django.urls import path
from . import views

urlpatterns = [
    # path("", views.movie_list, name="movie-list"),
    path("", views.Movies.as_view(), name="movie-list"),
    path("<int:pk>/", views.MovieDetail.as_view(), name="movie-dtail"),
]
