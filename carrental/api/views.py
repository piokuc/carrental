from rest_framework import generics
from .serializers import (CarSerializer, ReservationSerializer)
from .models import (Car, Reservation)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser)


class CarCreateView(generics.ListCreateAPIView):
    """Defines the car create functionality of our rest api."""
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Car.objects.all()

    def perform_create(self, serializer):
        """Save the post data when creating a new car."""
        serializer.save()


class CarDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminUser,)


class ReservationCreateView(generics.ListCreateAPIView):
    """Defines the reservation making functionality of our rest api."""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.all()

    def perform_create(self, serializer):
        """Save the post data when making a new reservation."""
        serializer.save()


class ReservationDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

