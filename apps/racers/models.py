from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Racer(AbstractUser):
    number = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(1)])
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1500, null=True, blank=True)
    score = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    year_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=70)
    stance = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.username}, #{self.number}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('racers:racer_detail', args=[self.pk])
