from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Car, Rating
from api.serializers import (
    CarCreateSerializer,
    CarListSerializer,
    CarPopularListSerializer,
    RateSerializer,
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

    def destroy(self, request, *args, **kwargs):
        pass


class RateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Rating.objects.all()
    serializer_class = RateSerializer


class PopularView(APIView):
    """View to list cars by the number of ratings."""

    def get_queryset(self):
        # TODO: get cars by the number of given rates
        return Car.object.order_by("-rating")

    def get(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        data = CarPopularListSerializer(queryset, many=True)
        return Response(data)
