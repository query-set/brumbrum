from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import CarViewSet, RateView, PopularView

router = routers.DefaultRouter(trailing_slash=False)
router.register("cars", CarViewSet, basename="cars")
router.register("rate", RateView, basename="rate")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("popular", PopularView.as_view(), name="popular"),
    path("", include(router.urls)),
]
