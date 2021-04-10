from django.contrib import admin

from api.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["make", "model"]
    search_fields = ["make", "model"]
    ordering = ["make"]
