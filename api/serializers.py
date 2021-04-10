from rest_framework import serializers

from api.models import Car


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["make", "model"]


class CarListSerializer(serializers.ModelSerializer):
    # Review note:
    # whole serializer could be inherited from `CarCreateSerializer`
    # but I wanted to be sure with the Meta.fields order.
    class Meta:
        model = Car
        fields = ["id", "make", "model", "avg_rating"]
