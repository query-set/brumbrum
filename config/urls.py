"""brumbrum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import CarViewSet, RateView, PopularView

router = routers.DefaultRouter()
router.register("cars", CarViewSet, basename="cars")
router.register("rate", RateView, basename="rate")

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("rate", RateView.as_view({"post": "create"}), name="rate"),
    path("popular/", PopularView.as_view(), name="popular"),
    path("", include(router.urls)),
]
