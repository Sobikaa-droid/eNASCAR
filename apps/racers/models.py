import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Racer(AbstractUser):
    number = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(1)])
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1500, null=True, blank=True)
    score = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    active_since = models.DateField(auto_now_add=True)
    year_of_birth = models.DateField(null=True, blank=True)
    stance = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.first_name} {self.second_name} ({self.username} {self.number})'

    def save(self, *args, **kwargs):
        # set the racer's number to random one cuz why the fuck not
        # if not self.pk and not self.number:
        #     self.number = random.randint(1, 99)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('racers:racer_detail', args=[self.pk])
