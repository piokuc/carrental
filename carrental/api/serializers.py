from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    """Serializer to map the Car model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Car
        fields = ('id', 'registration_number', 'make', 'model', 'photo')
