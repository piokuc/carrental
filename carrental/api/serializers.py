from rest_framework import serializers
from django.shortcuts import get_object_or_404 
from .models import (Car, Reservation)


class CarSerializer(serializers.ModelSerializer):
    """Serializer to map the Car model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Car
        fields = ('id', 'registration_number', 'make', 'model', 'photo')


class ReservationSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Reservation
        fields = ('id', 'customer', 'car', 'start', 'end', 'cancelled')

    def validate(self, data):
        """
        Check that start is before end.
        """
        if data['start'] > data['end']:
            raise serializers.ValidationError("end must occur after start")

        if data['end'] > data['start'] + datetime.timedelta(days=3):
            raise serializers.ValidationError("a car can only be reserved for up to 3 days")

        return data
