from django.db import models

from apps.racers.models import Racer
from django.urls import reverse


class Race(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1500, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(default=None, blank=True, null=True)
    racers = models.ManyToManyField(Racer, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('races:race_detail', args=[self.pk])
