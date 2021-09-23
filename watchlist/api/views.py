from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist.models import Movie
from .serializers import MovieSerializer


@api_view(['GET', 'POST'])
def movie_list(request):
    """Return Movie list response"""

    if request.method == "GET":
        movies = Movie.objects.all()
        serialized_data = MovieSerializer(movies, many=True)

        return Response(serialized_data.data)

    if request.method == "POST":
        serialized_data = MovieSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        else:
            return Response(serialized_data.errors)


@api_view(['GET', 'PUT', "DELETE"])
def movie_detail(request, pk):
    """Return the detail of a movie"""

    movie = Movie.objects.get(pk=pk)

    if request.method == "GET":
        serialized_data = MovieSerializer(movie)

        return Response(serialized_data.data)

    if request.method == "PUT":
        serialized_data = MovieSerializer(Movie, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        else:
            return Response(serialized_data.errors)

    if request.method == "DELETE":
        Movie.delete(movie)
        return Response({"Delete": "Item deleted successfully"})
