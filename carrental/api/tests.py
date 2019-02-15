from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import datetime

from .models import (Car, Reservation)
from django.contrib.auth import get_user_model
User = get_user_model()

# Admin user
TEST_ADMIN = 'piotr'
TEST_PASSWORD = 'secret'

class CarModelTestCase(TestCase):
    """
    Test suite for Car model.
    """

    def setUp(self):
        self.car = Car(registration_number = '903X252',
                       make = "renault",
                       model = "megane")


    def test_model_can_create_a_car(self):
        old_count = Car.objects.count()
        self.car.save()
        new_count = Car.objects.count()
        self.assertEqual(old_count + 1, new_count)



class CarViewTestCase(TestCase):
    """Test suite for the car api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.client.login(username=TEST_ADMIN, password=TEST_PASSWORD)
        self.car_data = {'registration_number': 'APL 911H',
                         'make': 'Reliant Regal',
                         'model': 'Supervan II'}
        self.response = self.client.post(reverse('create'),
                                         self.car_data,
                                         format="json")


    def test_api_can_create_a_car(self):
        """Test the api has car creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


    def test_api_can_get_a_car(self):
        """Test the api can get a given car."""
        car = Car.objects.get()
        response = self.client.get(reverse('details', kwargs={'pk': car.id}),
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, car.model)


    def test_api_can_delete_car(self):
        """Test the api can delete a car."""
        car = Car.objects.get()
        response = self.client.delete(reverse('details', kwargs={'pk': car.id}),
                                      format='json',
                                      follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)



class ReservationModelTestCase(TestCase):
    """
    Test suite for Reservation model.
    """

    def setUp(self):
        self.user = User.objects.create_user('test@example.com', 'testuser', 'testpassword')
        self.user.save()
        self.car = Car(registration_number = '903X252',
                       make = "renault",
                       model = "megane")
        self.car.save()

        self.reservation = Reservation(customer = self.user,
                                       car = self.car,
                                       start = datetime.date.today(),
                                       end = datetime.date.today() + datetime.timedelta(days=1),
                                       cancelled = False)


        old_count = Reservation.objects.count()
        self.reservation.save()
        new_count = Reservation.objects.count()
        self.assertEqual(old_count + 1, new_count)


    def test_api_can_get_a_reservation(self):
        """Test the api can get a reservation."""
        reservation = Reservation.objects.get()
        response = self.client.get(reverse('reservation_details', kwargs={'pk': self.reservation.id}),
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.reservation.id)
