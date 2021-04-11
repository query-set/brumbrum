import json
from urllib.request import urlopen

from rest_framework import serializers

from api.models import Car, Rating


VEHICLES_API = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"

# Review note:
# whole serializer could be inherited from `CarCreateSerializer`
# but I wanted to be sure with the Meta.fields order.


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["make", "model"]

    def validate(self, attrs):
        make = attrs.get("make").lower()
        model = attrs.get("model").lower()

        url = VEHICLES_API.format(make)
        response = urlopen(url)
        if response.code != 200:
            raise serializers.ValidationError("Cannot connect to API.")
        api_data = json.load(response)
        if len(api_data["Results"]) == 0:
            raise serializers.ValidationError(f"Cannot find models with '{make}' make.")
        all_models = [m["Model_Name"].lower() for m in api_data["Results"]]
        if model not in all_models:
            raise serializers.ValidationError("Model not found.")

        if Car.objects.filter(make=make, model=model).exists():
            raise serializers.ValidationError(
                f"Car {make} {model} already exists in the database."
            )
        return {"make": make, "model": model}


class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "avg_rating"]


class CarPopularListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "rates_number"]


class RateSerializer(serializers.ModelSerializer):
    car_id = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ["car_id", "rating"]
