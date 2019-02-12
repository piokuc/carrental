from django.shortcuts import render

from rest_framework import generics
from .serializers import CarSerializer
from .models import Car
from rest_framework.permissions import IsAuthenticated


class CarCreateView(generics.ListCreateAPIView):
    """Defines the car create functionality of our rest api."""
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        return Car.objects.all()

    def perform_create(self, serializer):
        """Save the post data when creating a new car."""
        serializer.save()


class CarDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer

