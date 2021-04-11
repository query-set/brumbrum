from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    avg_rating = models.FloatField("average rating", null=True, blank=True)

    def __str__(self):
        return f"{self.make} - {self.model}"

    def recalculate_car_rating(self, car_id: int):
        rating = Rating.objects.filter(car_id=car_id).aggregate(models.Avg("rating"))
        self._meta.model.objects.filter(id=car_id).update(
            avg_rating=rating["rating__avg"]
        )


class Rating(models.Model):
    car_id = models.ForeignKey("Car", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def save(self, **kwargs):
        Car().recalculate_car_rating(self.car_id.pk)
        super().save(**kwargs)
