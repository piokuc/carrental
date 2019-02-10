from django.test import TestCase

from .models import Car


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
