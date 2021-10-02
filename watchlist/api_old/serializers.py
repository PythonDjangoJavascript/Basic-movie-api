from watchlist.models import Movie
from rest_framework import serializers


class MovieModelSerializer(serializers.ModelSerializer):
    """Serialize our Movie Model"""

    name_len = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ['id', ]

    def get_name_len(self, object):
        """Define custom name lenght field"""
        return len(object.name)

    def validate(self, attrs):
        """Validate object"""

        if attrs["name"] == attrs["descripiton"]:
            raise serializers.ValidationError(
                "Name and descripiton can't be same")

        return attrs

    def validate_name(self, value):
        """Validate Name input"""

        if len(value) < 3:
            raise serializers.ValidationError("Name Is Too short")

        return value


def is_four_char_str(attrs):
    """validate string to have at leat 4 charecter"""

    if len(attrs) < 4:
        raise serializers.ValidationError(
            "Should be at least 4 char long")


class MovieSerializer(serializers.Serializer):
    """Serializes Movie data"""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[is_four_char_str])
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

    def validate(self, attrs):
        """Validate object"""

        if attrs["name"] == attrs["descripiton"]:
            raise serializers.ValidationError(
                "Name and descripiton can't be same")

        return attrs

    # its field level validator but there is a better solution for this
    # and I used that solution for name validation
    # def validate_name(self, value):
    #     """Validate Name input"""

    #     if len(value) < 3:
    #         raise serializers.ValidationError("Name Is Too short")

    #     return value

    # Model Serializer
