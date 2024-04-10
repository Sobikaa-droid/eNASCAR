from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import Car, Racer


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class RacerSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Racer
        fields = ['id', 'number', 'username', 'password', 'first_name', 'second_name', 'description', 'wins', 'loses',
                  'car']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        car_data = validated_data.pop('car')
        car_serializer = self.fields['car']
        car_instance = car_serializer.create(car_data)
        validated_data['car'] = car_instance
        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)

    def update(self, instance, validated_data):
        car_data = validated_data.pop('car')
        car_serializer = self.fields['car']
        car_instance = instance.car

        car_serializer.update(car_instance, car_data)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car'] = CarSerializer(instance.car).data

        return representation
