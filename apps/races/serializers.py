from rest_framework import serializers

from .models import Race
from apps.racers.serializers import RacerSerializer


class RaceSerializer(serializers.ModelSerializer):
    racers = RacerSerializer(many=True, required=False)

    class Meta:
        model = Race
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     racer = self.context['request'].user
    #     racers_numbers = instance.racers.values_list('number', flat=True)
    #
    #     if not racer.is_staff:
    #         if not racer.first_name or not racer.last_name:
    #             raise serializers.ValidationError("You don't have a first/last name.")
    #         if not racer.car:
    #             raise serializers.ValidationError("You don't have a car.")
    #         if racer.number in racers_numbers:
    #             raise serializers.ValidationError(f"The number {racer.number} is already registered to this race. "
    #                                               f"Change your number.")
    #
    #     super().update(instance, validated_data)
