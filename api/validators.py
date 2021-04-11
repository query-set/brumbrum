from rest_framework import serializers

from api.models import Car


def validate_if_car_exists(data: dict, make: str, model: str):
    if len(data["Results"]) == 0:
        raise serializers.ValidationError(f"Cannot find models with '{make}' make.")
    all_models = [m["Model_Name"].lower() for m in data["Results"]]
    if model not in all_models:
        raise serializers.ValidationError("Model not found.")


def validate_new_car(make: str, model: str):
    if Car.objects.filter(make=make, model=model).exists():
        raise serializers.ValidationError(
            f"Car {make} {model} already exists in the database."
        )
