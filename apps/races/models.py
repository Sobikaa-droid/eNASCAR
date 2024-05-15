from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from apps.racers.models import Racer


class Race(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=1500, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    racers = models.ManyToManyField(Racer, blank=True, through='RaceEntry')
    race_limit = models.IntegerField(default=10, validators=[MaxValueValidator(100), MinValueValidator(2)])

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
    place = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.racer} - {self.race}"
