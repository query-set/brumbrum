import json
from urllib.request import urlopen

from rest_framework import serializers

from api.models import Car


VEHICLES_API = (
    "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"
)

# Review note:
# whole serializer could be inherited from `CarCreateSerializer`
# but I wanted to be sure with the Meta.fields order.


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["make", "model"]

    def validate(self, attrs):
        url = VEHICLES_API.format(attrs.get("make").lower())
        response = urlopen(url)
        if response.code != 200:
            raise serializers.ValidationError("Cannot connect to API.")
        api_data = json.load(response)
        if len(api_data["Results"]) == 0:
            raise serializers.ValidationError(
                f"Cannot find models with '{attrs['make']}' make."
            )
        all_models = [m["Model_Name"].lower() for m in api_data["Results"]]
        if attrs["model"].lower() not in all_models:
            raise serializers.ValidationError("Model not found.")
        return attrs


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
