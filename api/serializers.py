from rest_framework import serializers

from api.models import Car


# Review note:
# whole serializer could be inherited from `CarCreateSerializer`
# but I wanted to be sure with the Meta.fields order.


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["make", "model"]


class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "avg_rating"]


class CarPopularListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "rates_number"]


class RateSerializer(serializers.Serializer):
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    rating = serializers.IntegerField(min_value=1, max_value=5)
