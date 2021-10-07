from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import filters
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.throttling import (
    UserRateThrottle, AnonRateThrottle, ScopedRateThrottle)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (
    status, mixins, generics)
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from watchlist.api.permissions import AdminOrReadOnly, ReviewOwnerOrReadOnly
from watchlist.models import Review, WatchList, StreamPlatform
from watchlist.api.serializers import (
    ReviewSerializer, WatchlistSerializer, StreamPlatformSerializer)
from watchlist.api.throttling import *
from watchlist.api.pagination import (
    StanderdCursorPagination,
    StanderedPNumPagination,
    StanderdLimitOffsetPagination
)


class UserReview(generics.ListAPIView):
    """Returns all reivews posted by a user"""
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrReadOnly]

    # def get_queryset(self):
    #     """Filter query by user info form url argument"""

    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username = username)

    def get_queryset(self):
        """Filter query by username from query params"""

        username = self.request.query_params.get('username', None)

        if username is not None:
            return Review.objects.filter(review_user__username=username)
        raise ValidationError("Username Not Found", status.HTTP_404_NOT_FOUND)


class ReviewListAPIView(generics.ListCreateAPIView):
    """Response review list and create review"""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly, ]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def update_movie_reivew_count(self, movie_obj, rating):
        """Update movie object with provided raring"""
        try:
            movie_obj.total_reviews += 1
            movie_obj.avg_rating = (
                movie_obj.avg_rating + rating)/movie_obj.total_reviews
            movie_obj.save()
        except Exception as e:
            raise ValidationError("Could not update the rating!")

    def get_queryset(self):
        """Overriding queryset to perform fetch review operation only for
        selected movie"""

        # filter query only for selected movie
        queryset = Review.objects.filter(
            watchlist=self.kwargs['pk'])
        return queryset

    def perform_create(self, serializer):
        """Overriding create method to create reviews only for selected movie"""
        logged_user = self.request.user
        selected_movie = WatchList.objects.get(pk=self.kwargs.get('pk'))

        # youser arleady reviewed?
        logged_user_query = Review.objects.filter(
            watchlist=selected_movie, review_user=logged_user)
        if logged_user_query.exists():
            raise ValidationError("You already reviewed this Movie!")

        # now update movie obj ratings detail
        rating = serializer.validated_data['rating']
        self.update_movie_reivew_count(selected_movie, rating)

        # Save Review
        serializer.save(watchlist=selected_movie,
                        review_user=logged_user)

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

    permission_classes = [ReviewOwnerOrReadOnly, ]
    throttle_classes = [UserReviewDetailThrottle, ]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def get_queryset(slef):
    #     # Overriding query method to include user


# class ReviewDetailAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     """Response Movie Review Detail"""

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         """Returns reviews detail response and allow get request"""
#         return self.retrieve(request, *args, **kwargs)


class WatchListFilterAPIView(generics.ListAPIView):
    """Response Filtered Movielist"""

    queryset = WatchList.objects.all()
    serializer_class = WatchlistSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['title', 'platform__name', ]
    search_fields = ['title', ]
    ordering_fields = ['avg_rating', ]

    # pagination_class = StanderedPNumPagination
    pagination_class = StanderdLimitOffsetPagination
    # pagination_class = StanderdCursorPagination


class WatchlistAPIView(APIView):
    """Response with watch list data"""

    permission_classes = [AdminOrReadOnly, ]

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

    permission_classes = [AdminOrReadOnly, ]
    throttle_classes = [WatchDetailThrottle, ]

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
class StreamPlatformViewSets(ModelViewSet):
    """Manages crud responses on stram object"""
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class StreamPlatformViewSetsOLD(ViewSet):
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

    def create(self, request):
        # crate new stramPlatform obj
        serialized_data = StreamPlatformSerializer(data=request.data)
        if serialized_data.is_valid():
            # Save the model
            serialized_data.save()
            return Response(serialized_data.data)
        return Response(serialized_data.errors)


class StreamPlatformAPIView(APIView):
    """Manages Strea platform api views responses"""

    permission_classes = [AdminOrReadOnly, ]

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

    permission_classes = [AdminOrReadOnly, ]
    throttle_classes = [ScopedRateThrottle, ]
    throttle_scope = 'stream-detail'

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
