from watchlist.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    """Serializes Movie data"""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    descripiton = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        """Add new movie from post request"""

        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a movie object"""
        """It will update the movie with validated data and if data is not given
        it will set the default data"""

        instance.name = validated_data.get("name", instance.name)
        instance.descripiton = validated_data.get(
            "descripiton", instance.descripiton)
        instance.active = validated_data.get("active", instance.active)

        instance.save()

        return instance
