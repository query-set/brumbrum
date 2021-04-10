from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Car
from api.serializers import (
    CarCreateSerializer,
    CarListSerializer,
    CarPopularListSerializer,
)


class CarViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "list": CarListSerializer,
        "create": CarCreateSerializer,
    }
    default_serializer_class = CarListSerializer
    queryset = Car.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def post(self, request, *args, **kwargs) -> Response:
        # TODO
        # validate the model existence against following page:
        # https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/honda?format=json
        return None


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
