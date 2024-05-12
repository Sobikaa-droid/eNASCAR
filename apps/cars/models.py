from django.db import models

from apps.racers.models import Racer
from django.urls import reverse


class CarModel(models.Model):
    name = models.CharField(max_length=75)
    speed = models.IntegerField()
    date_of_manufacture = models.DateField()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.name} - {self.date_of_manufacture} ({self.speed} km/h)'


class Car(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    color = models.CharField(max_length=75)
    racer = models.OneToOneField(Racer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.car_model

    def get_absolute_url(self):
        return reverse('cars:car_detail', args=[self.pk])
