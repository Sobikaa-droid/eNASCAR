from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Car


@receiver(pre_delete, sender=Car)
def pre_delete_model(sender, instance, **kwargs):
    racer = instance.racer
    active_races = racer.race_set.filter(completion_date__isnull=True)
    if active_races.exists():
        active_races.first().racers.remove(racer)
