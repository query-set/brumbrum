from django.contrib import admin

from api.models import Car, Rating


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model"]
    search_fields = ["make", "model"]
    ordering = ["make"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
