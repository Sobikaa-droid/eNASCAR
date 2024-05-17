from rest_framework import serializers

from .models import Race, RaceEntry
from apps.racers.serializers import RacerSerializer


class RaceSerializer(serializers.ModelSerializer):
    racers = RacerSerializer(many=True, required=False)

    class Meta:
        model = Race
        fields = '__all__'


class RaceEntrySerializer(serializers.ModelSerializer):
    racer = RacerSerializer(many=False, required=False)
    race = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RaceEntry
        fields = '__all__'
