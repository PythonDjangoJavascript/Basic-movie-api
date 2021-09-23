from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from watchlist.models import Movie
from .serializers import MovieSerializer


class Movies(APIView):
    """Response with movie list"""

    def get(self, request):
        try:
            movies = Movie.objects.all()
        except Movie.DoesNotExist:
            return Response({"Error": "Movie Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = MovieSerializer(movies, many=True)

        return Response(serialized_data.data)

    def post(self, request):
        serialized_data = MovieSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetail(APIView):
    """Response Movie Detail API"""

    def get(self, request, pk):
        """return movie detail response"""

        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = MovieSerializer(movie)

        return Response(serialized_data.data)

    def put(self, request, pk):
        """Updated Movie"""
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = MovieSerializer(movie, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete single movie"""
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        Movie.delete(movie)
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     """Return Movie list response"""

#     if request.method == "GET":
#         try:
#             movies = Movie.objects.all()
#         except Movie.DoesNotExist:
#             return Response({"Error": "Movie Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

#         serialized_data = MovieSerializer(movies, many=True)

#         return Response(serialized_data.data)

#     if request.method == "POST":
#         serialized_data = MovieSerializer(data=request.data)

#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data)
#         else:
#             return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', "DELETE"])
# def movie_detail(request, pk):
#     """Return the detail of a movie"""

#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error": "Movie Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serialized_data = MovieSerializer(movie)

#         return Response(serialized_data.data)

#     if request.method == "PUT":
#         serialized_data = MovieSerializer(movie, data=request.data)
#         if serialized_data.is_valid():
#             serialized_data.save()
#             return Response(serialized_data.data)
#         else:
#             return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == "DELETE":
#         Movie.delete(movie)
#         return Response(status=status.HTTP_204_NO_CONTENT)
