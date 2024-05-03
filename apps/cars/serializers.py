from rest_framework import serializers

from .models import Car


class CarSerializer(serializers.ModelSerializer):
    racer = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = '__all__'
