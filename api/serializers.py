import json
import socket
from urllib.request import urlopen

from rest_framework import serializers

from api.models import Car, Rating
from api.validators import validate_if_car_exists, validate_new_car


VEHICLES_API = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"
TIMEOUT = 5

# Review note:
# whole serializer could be inherited from `CarCreateSerializer`
# but I wanted to be sure with the Meta.fields order.


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["make", "model"]

    @staticmethod
    def get_api_data(url: str) -> dict:
        try:
            response = urlopen(url, timeout=TIMEOUT)
        except socket.timeout as e:
            raise serializers.ValidationError(e)

        if response.code != 200:
            raise serializers.ValidationError("Cannot connect to API.")
        return json.load(response)

    def validate(self, attrs):
        make = attrs.get("make").lower()
        model = attrs.get("model").lower()
        url = VEHICLES_API.format(make)
        api_data = self.get_api_data(url)

        validate_if_car_exists(api_data, make, model)
        validate_new_car(make, model)

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
