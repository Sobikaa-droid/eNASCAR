from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.racers.models import Racer


# class RaceManager(models.Manager):
#     def complete_race(self, pk):
#         obj = self.get_queryset().prefetch_related('racers').get(pk=pk)
#         racers = obj.racers.all().order_by('car__car_model__speed')
#         if racers.count() == obj.race_limit and obj.completion_date is None:
#             race_entry = RaceEntry.objects.all()
#             racers_ids = [racer.id for racer in racers]
#             for position, racer_id in enumerate(racers_ids, start=1):
#                 racer_entry = race_entry.get(race=obj, racer_id=racer_id)
#                 racer_entry.position = position
#                 racer_entry.save()
#             for racer in racers:
#                 racer_entry = race_entry.select_related('racer').filter(racer=racer)
#                 race_entry_obj = racer_entry.get(race=obj)
#                 race_entry_obj.racer.score = (obj.race_limit - race_entry_obj.position + 1) / racer_entry.count()
#                 race_entry_obj.racer.save()
#             obj.completion_date = timezone.now()
#             obj.save()


class Race(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1500, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    racers = models.ManyToManyField(Racer, blank=True, through='RaceEntry')
    race_limit = models.IntegerField(default=10, validators=[MaxValueValidator(100), MinValueValidator(2)])

    # objects = RaceManager()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('races:race_detail', args=[self.pk])


# @receiver(m2m_changed, sender=Race.racers.through)
# def regions_changed(sender, **kwargs):
#     if kwargs['instance'].racers.count() > kwargs['instance'].race_limit:
#         raise ValidationError(f"You can't assign more than {kwargs['instance'].race_limit}")


class RaceEntry(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    position = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.racer} - {self.race}"
