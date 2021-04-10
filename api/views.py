import json
from urllib.request import urlopen
from typing import Dict

from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Car
from api.serializers import (
    CarCreateSerializer,
    CarListSerializer,
    CarPopularListSerializer,
)


VALIDATION_API = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json"


class CarViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    default_serializer_class = CarListSerializer
    permission_classes = [AllowAny]
    queryset = Car.objects.all()
    serializer_classes = {
        "list": CarListSerializer,
        "create": CarCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs) -> Response:
        self.validate_model_existence(request.data)
        serializer = CarCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: validate the model existence against following page:
        #
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def validate_model_existence(model_data: Dict[str, str]):
        url = VALIDATION_API.format(model_data.get("make"))
        response = urlopen(url)
        api_data = json.load(response)
        all_models = [m["Model_Name"] for m in api_data["Results"]]
        if model_data["model"] not in all_models:
            raise Error("Model not found")


class RateView(APIView):
    def post(self, request, *args, **kwargs) -> Response:
        # TODO
        return None


class PopularView(APIView):
    """View to list cars by the number of ratings."""

    def get_queryset(self):
        # TODO: get cars by the number of given rates
        return Car.object.order_by("-rating")

    def get(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        data = CarPopularListSerializer(queryset, many=True)
        return Response(data)
