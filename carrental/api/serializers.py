from rest_framework import serializers
from django.shortcuts import get_object_or_404 
from .models import (Car, Reservation)
import datetime


class CarSerializer(serializers.ModelSerializer):
    """Serializer to map the Car model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Car
        fields = ('id', 'registration_number', 'make', 'model', 'photo')


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ('id', 'customer', 'car', 'start', 'end', 'cancelled')

    def validate(self, data):
        """
        Validate reservation:
        - check that start of reservation is before its end,
        - reservation allowed for up to 3 days only,
        - cancellation is allowed only before reservation starts,
        - check the car is no already reserved fgor the dates.
        """
        start, end = data['start'], data['end']

        if start > end:
            raise serializers.ValidationError("end must occur after start")

        if end > start + datetime.timedelta(days=3):
            raise serializers.ValidationError("a car can only be reserved for up to 3 days")

        if data['cancelled'] and datetime.today() >= start:
            raise serializers.ValidationError("reservation can only be cancelled before it starts")

        car_reservations = Reservation.objects.all().filter(car=data['car'])
        if (len(car_reservations.filter(start__range=[start, end])) > 0
            or len(car_reservations.filter(end__range=[start, end])) > 0):
            raise serializers.ValidationError("the car is already reserved during the chosen period")

        return data
