from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    avg_rating = models.FloatField("average rating", null=True, blank=True)

    def __str__(self):
        return f"{self.make} - {self.model}"

    @property
    def rates_number(self) -> int:
        """Returns number of given rates on car."""
        return Rating.objects.filter(car_id=self.id).count()

    def recalculate_car_rating(self, car_id):
        query = Rating.objects.filter(car_id=car_id).aggregate(models.Avg("rating"))
        self._meta.model.objects.filter(id=car_id).update(
            avg_rating=query["rating__avg"]
        )


class Rating(models.Model):
    car_id = models.ForeignKey("Car", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def save(self, **kwargs):
        """On every car's rate change updates the car's average rating."""
        super().save(**kwargs)
        Car().recalculate_car_rating(self.car_id.pk)
