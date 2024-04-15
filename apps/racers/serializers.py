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
        car_data = validated_data['car']
        car_serializer = self.fields['car']
        car_instance = car_serializer.create(car_data)
        validated_data['car'] = car_instance
        racer = Racer.objects.create(**validated_data)
        racer.set_password(validated_data['password'])
        racer.save()

        return racer

    def update(self, instance, validated_data):
        # Update racer instances with the validated data
        instance.number = validated_data.get('number', instance.number)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.description = validated_data.get('description', instance.description)
        instance.car = validated_data.get('car', instance.car)

        # Check if password is provided and update it if necessary
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['car'] = CarSerializer(instance.car).data

        return representation
