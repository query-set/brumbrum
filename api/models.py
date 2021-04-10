from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Rating(models.Model):
    car_id = models.ForeignKey("Car", on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class Car(models.Model):
    make = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    avg_rating = models.FloatField("average rating")

    def __str__(self):
        return f"{self.make} - {self.model}"

    def save(self, *args, **kwargs):
        # TODO: proper set the id
        self.avg_rating = self.calculate_avg_rating(self.id)
        return super().save(*args, **kwargs)

    @staticmethod
    def calculate_avg_rating(car_id: int) -> float:
        rating_query = Rating.objects.filter(car_id=car_id)
        # TODO calculate the rating query
        return 0
