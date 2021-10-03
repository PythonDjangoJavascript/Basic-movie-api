from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (
    status, mixins, generics
)
from rest_framework.viewsets import ViewSet

from watchlist.models import Review, WatchList, StreamPlatform
from watchlist.api.serializers import (
    ReviewSerializer, WatchlistSerializer, StreamPlatformSerializer
)


class ReviewListAPIView(generics.ListCreateAPIView):
    """Response review list and create review"""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Overriding queryset to perform fetch review operation only for
        selected movie"""

        # filter query only for selected movie
        queryset = Review.objects.filter(watchlist=self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        """Overriding create method to create reviews only for selected movie"""

        selected_movie = WatchList.objects.get(pk=self.kwargs.get('pk'))

        serializer.save(watchlist=selected_movie)

# class ReviewListAPIView(mixins.ListModelMixin,
#                         mixins.CreateModelMixin,
#                         generics.GenericAPIView):
#     """Return reviews list and create a new Review"""

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve Reveiw detail through get request and update and delete 
    existing review"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# class ReviewDetailAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     """Response Movie Review Detail"""

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         """Returns reviews detail response and allow get request"""
#         return self.retrieve(request, *args, **kwargs)


class WatchlistAPIView(APIView):
    """Response with watch list data"""

    def get(self, request):
        try:
            watchlist = WatchList.objects.all()
        except WatchList.DoesNotExist:
            return Response({
                "Error": "List Does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        # serealize data if found
        serialized_data = WatchlistSerializer(
            watchlist, many=True)

        return Response(serialized_data.data)

    def post(self, request):
        serialized_data = WatchlistSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )


class WatchDetailAPIView(APIView):
    """Returns Movie Detail from wathlist"""

    def get(self, request, pk):
        """Returns Movie detail"""

        try:
            watch_item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({
                "Error": "Does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serialized_data = WatchlistSerializer(watch_item)

        return Response(serialized_data.data)

    def put(self, request, pk):
        try:
            watch_item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({
                "Error": "Does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        serialized_data = WatchlistSerializer(watch_item, data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            watch_item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({
                "Error": "Does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        WatchList.delete(watch_item)
        return Response(status=status.HTTP_204_NO_CONTENT)


# StreamPlatform
class StreamPlatformViewSets(ViewSet):
    """Manages stream api response list and detail"""

    def list(self, request):
        # Get Request
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Get Detail View
        queryset = StreamPlatform.objects.all()
        platform_single = get_object_or_404(queryset, pk=pk)
        serialized_data = StreamPlatformSerializer(platform_single)
        return Response(serialized_data.data)


class StreamPlatformAPIView(APIView):
    """Manages Strea platform api views responses"""

    def get(self, request):
        try:
            platforms = StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist:
            return Response({
                "Error": "No Platform found"
            }, status=status.HTTP_404_NOT_FOUND)

        # if found
        serialized_data = StreamPlatformSerializer(
            platforms, many=True, context={'request': request})
        return Response(serialized_data.data)

    def post(self, request):
        serialized_data = StreamPlatformSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )


class StreamPlatformDetialAPIView(APIView):
    """Manages Stream Platform Detail Api Responses"""

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({
                "Error": "Platform not found"
            }, status=status.HTTP_404_NOT_FOUND)
        # if found the platfor with pk
        serialized_data = StreamPlatformSerializer(platform)
        return Response(serialized_data.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({
                "Error": "Does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        # when object found with pk
        serialized_data = StreamPlatformSerializer(platform, data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(
            serialized_data.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({
                "Error": "Does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        # when object found with pk
        StreamPlatform.delete(platform)
        return Response(status=status.HTTP_204_NO_CONTENT)
