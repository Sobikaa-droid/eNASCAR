from rest_framework import serializers

from .models import Race
from apps.racers.serializers import RacerSerializer


class RaceSerializer(serializers.ModelSerializer):
    racers = RacerSerializer(many=True, required=False)

    class Meta:
        model = Race
        fields = '__all__'
