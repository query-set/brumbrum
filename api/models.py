from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=55)
    model = models.CharField(max_length=55)
    avg_rating = models.FloatField()

    def __str__(self):
        return f"{self.make} - {self.model}"
