from watchlist.models import StreamPlatform, WatchList
from rest_framework import serializers


class WatchlistSerializer(serializers.ModelSerializer):
    """Serializes Watchlist model"""

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
