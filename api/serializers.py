import json
from urllib.request import urlopen

from rest_framework import serializers

from api.models import Car


VALIDATION_API = (
    "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"
)

# Review note:
# whole serializer could be inherited from `CarCreateSerializer`
# but I wanted to be sure with the Meta.fields order.


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["make", "model"]

    def validate(self, data):
        url = VALIDATION_API.format(data.get("make").lower())
        response = urlopen(url)
        api_data = json.load(response)
        all_models = [m["Model_Name"].lower() for m in api_data["Results"]]
        if data["model"].lower() not in all_models:
            raise serializers.ValidationError("Model not found")
        return data


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
