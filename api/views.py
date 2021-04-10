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
        serializer = CarCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
