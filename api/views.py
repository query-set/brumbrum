from rest_framework import mixins, viewsets

from api.models import Car
from api.serializers import CarCreateSerializer, CarListSerializer


class CarViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_classes = {
        "list": CarListSerializer,
        "create": CarCreateSerializer,
        # "destroy": CarCreateSerializer,
    }
    default_serializer_class = CarListSerializer
    queryset = Car.objects.all()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    # def create(self, request, *args, **kwargs):
    #     return
