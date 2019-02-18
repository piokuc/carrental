from rest_framework import serializers
from django.shortcuts import get_object_or_404 
from .models import (Car, Reservation)
import datetime


class CarSerializer(serializers.ModelSerializer):
    """
    Serializer to map the Car model instance into JSON format.
    """

    available_now = serializers.SerializerMethodField()
    currently_reserved_by = serializers.SerializerMethodField()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Car
        fields = ('id', 'registration_number', 'make', 'model',
                  'available_now', 'currently_reserved_by',
                  'photo')

    def get_available_now(self, car):
        reservations = Reservation.objects.filter(car=car)
        today = datetime.datetime.now()
        return reservations.filter(start__lte=today, end__gte=today).count() == 0


    def get_currently_reserved_by(self, car):
        if self.get_available_now(car):
            return None
        reservations = Reservation.objects.filter(car=car)
        today = datetime.datetime.now()
        current_reservation = reservations.filter(start__lte=today, end__gte=today).get()
        return current_reservation.customer.username


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for Reservation objects.
    Converts from and to JSON, validates new reservations.
    """

    class Meta:
        model = Reservation
        fields = ('id', 'customer', 'car', 'start', 'end', 'cancelled')

    def validate(self, data):
        """
        Validate reservation:
        - check that start of reservation is before its end,
        - reservation allowed for up to 3 days only,
        - cancellation is allowed only before reservation starts,
        - check the car is not already reserved for the dates.
        """
        start, end = data['start'], data['end']

        if start > end:
            raise serializers.ValidationError("end must occur after start")

        if end > start + datetime.timedelta(days=3):
            raise serializers.ValidationError("car can only be reserved for up to 3 days")

        if data['cancelled'] and datetime.today() >= start:
            raise serializers.ValidationError("reservation can only be cancelled before it starts")

        car_reservations = Reservation.objects.all().filter(car=data['car'])
        if (car_reservations.filter(start__range=[start, end]).count() > 0
            or car_reservations.filter(end__range=[start, end]).count() > 0):
            raise serializers.ValidationError("the car is already reserved during the chosen period")

        return data
