from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
import datetime
import json

from .models import (Car, Reservation)
from django.contrib.auth import get_user_model
User = get_user_model()

# Admin user
TEST_USER = 'piotr'
TEST_PASSWORD = 'secret'
TEST_EMAIL = "piotr@carrental.com"

TEST_USER2 = 'peter'
TEST_PASSWORD2 = 'secret'
TEST_EMAIL2 = "peter@carrental.com"

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
        self.test_user = get_user_model().objects.create_superuser(TEST_USER, TEST_EMAIL, TEST_PASSWORD)
        self.client = APIClient()
        self.client.login(username=TEST_USER, password=TEST_PASSWORD)
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


    def test_api_car_is_available_if_no_reservations(self):
        car = Car.objects.get()
        response = self.client.get(reverse('details', kwargs={'pk': car.id}),
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_content = json.loads(response.content)
        self.assertEqual(response_content['available_now'], True)
        self.assertEqual(response_content['currently_reserved_by'], None)


    def test_api_car_is_not_available_if_reserved(self):
        """
        Reserve a car from today to tomorrow, then check it is not availale.
        """
        car = Car.objects.get()
        reservation = Reservation(customer = self.test_user,
                                  car = car,
                                  start = datetime.date.today(),
                                  end = datetime.date.today() + datetime.timedelta(days=1),
                                  cancelled = False)
        reservation.save()

        response = self.client.get(reverse('details', kwargs={'pk': car.id}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_content = json.loads(response.content)
        self.assertEqual(response_content['available_now'], False)
        self.assertEqual(response_content['available_now'], False)
        self.assertEqual(response_content['currently_reserved_by'], TEST_USER)


class ReservationModelTestCase(TestCase):
    """
    Test suite for Reservation model.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(TEST_USER, TEST_EMAIL, TEST_PASSWORD)
        self.client = APIClient()
        self.client.login(username=TEST_USER, password=TEST_PASSWORD)
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


    def test_api_does_not_allow_duplicated_car_reservation(self):
        reservation_data = dict(customer = self.user.pk,
                                car = self.car.pk,
                                start = datetime.date.today() + datetime.timedelta(days=1),
                                end = datetime.date.today() + datetime.timedelta(days=2),
                                cancelled = False)
        response = self.client.post(reverse('make_reservation'), reservation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PDFGenerationModelTestCase(TestCase):
    """
    Test suite for the PDF Contract view
    """

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(TEST_USER, TEST_EMAIL, TEST_PASSWORD)
        self.user2 = get_user_model().objects.create_user(TEST_USER2, TEST_EMAIL2, TEST_PASSWORD2)
        self.client = APIClient()
        self.client.login(username=TEST_USER, password=TEST_PASSWORD)
        self.car = Car(registration_number = '903X252',
                       make = "renault",
                       model = "megane")
        self.car.save()

        self.reservation = Reservation(customer = self.user,
                                       car = self.car,
                                       start = datetime.date.today(),
                                       end = datetime.date.today() + datetime.timedelta(days=1),
                                       cancelled = False)

        self.reservation.save()


    def test_api_can_get_a_pdf_contract(self):
        """Test the PDF contract can be retrieved by staff."""
        response = self.client.get(reverse('pdf_contracts', kwargs={'pk': self.reservation.id}),
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')


    def test_api_does_not_give_a_pdf_contract_to_wrong_user(self):
        """
        Test the PDF contract cannot be retrieved by non staff users.
        """
        self.client.login(username=TEST_USER2, password=TEST_PASSWORD2)

        response = self.client.get(reverse('pdf_contracts', kwargs={'pk': self.reservation.id}),
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
