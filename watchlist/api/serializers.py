from watchlist.models import StreamPlatform, WatchList
from rest_framework import serializers


class WatchlistSerializer(serializers.ModelSerializer):
    """Serializes Watchlist model"""

    class Meta:
        model = WatchList
        exclude = ['crated_at', ]


class StreamPlatformSerializer(serializers.ModelSerializer):
    """Serializes Sream platform model"""

    class Meta:
        model = StreamPlatform
        fields = '__all__'
