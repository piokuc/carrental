from rest_framework import generics
from .serializers import (CarSerializer, ReservationSerializer)
from .models import (Car, Reservation)
from rest_framework.permissions import (IsAuthenticated, IsAdminUser)
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_list_or_404, get_object_or_404


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


def generate_contract(reservation):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    disposition = 'attachment; filename="car_reservation_no_%s.pdf"'.format(reservation.id)
    response['Content-Disposition'] = disposition 

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 200, "Car reservation no {}.".format(reservation.id))
    car = reservation.car
    p.drawString(100, 150, "Car registration number: {}, {} {}.".format(
                 car.registration_number, car.make, car.model))
    p.drawString(100, 130, "Reservation from {} to {}.".format(reservation.start, reservation.end))
    p.drawString(100, 100, "Signature:")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


@login_required
@api_view(['GET'])
def pdf_contract_view(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    response = generate_contract(reservation)
    return response
