import random

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from apps.racers.models import Racer


class RaceManager(models.Manager):
    def complete_race(self, pk):
        obj = self.get_queryset().prefetch_related('racers').get(pk=pk)
        racers = obj.racers.annotate(num_races=Count("race"))
        if len(racers) == obj.race_limit and obj.completion_date is None:
            randomized_dict = {index + 1: element for index, element in enumerate(
                random.sample(list(racers), obj.race_limit)
            )}
            for place, racer in randomized_dict.items():
                racer.score = (obj.race_limit - place + 1) / int(racer.num_races)
                racer.save()
            randomized_dict = {index + 1: f'{element.username} #{element.number}' for index, element in enumerate(
                random.sample(list(racers), obj.race_limit)
            )}
            obj.finished_racers = randomized_dict
            obj.completion_date = timezone.now()
            obj.save()


class Race(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1500, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(default=None, blank=True, null=True)
    racers = models.ManyToManyField(Racer, blank=True)
    finished_racers = models.JSONField(default=None, blank=True, null=True)
    race_limit = models.IntegerField(default=10, validators=[MaxValueValidator(100), MinValueValidator(2)])

    objects = RaceManager()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('races:race_detail', args=[self.pk])


@receiver(m2m_changed, sender=Race.racers.through)
def regions_changed(sender, **kwargs):
    if kwargs['instance'].racers.count() > kwargs['instance'].race_limit:
        raise ValidationError(f"You can't assign more than {kwargs['instance'].race_limit} regions")

