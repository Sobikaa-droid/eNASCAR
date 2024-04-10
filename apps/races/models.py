from django.db import models

from apps.racers.models import Racer
from django.urls import reverse


class Race(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    date_of_completion = models.DateTimeField(default=None, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    racers = models.ManyToManyField(Racer, blank=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('races:race_detail', args=[self.pk])
