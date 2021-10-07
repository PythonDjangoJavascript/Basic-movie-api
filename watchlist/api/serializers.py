from watchlist.models import Review, StreamPlatform, WatchList
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    """Serializes Reivew model fields"""

    review_user = serializers.StringRelatedField()
    watchlist = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('active',)


class WatchlistSerializer(serializers.ModelSerializer):
    """Serializes Watchlist model"""

    reviews = ReviewSerializer(many=True, read_only=True)
    # platform = serializers.CharField(source='platform.name')
    platform = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WatchList
        exclude = ['crated_at', ]


class StreamPlatformSerializer(serializers.ModelSerializer):
    """Serializes Sream platform model"""

    watchlist = WatchlistSerializer(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )

    class Meta:
        model = StreamPlatform
        fields = '__all__'
