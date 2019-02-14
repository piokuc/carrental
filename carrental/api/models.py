from django.db import models
from django.contrib.auth import get_user_model

class Car(models.Model):
    """
    Represents a car owned by the car rental company.
    """
    registration_number = models.CharField(max_length=10, blank=False, unique=True)
    make = models.CharField(max_length=255, blank=False)
    model = models.CharField(max_length=255, blank=False)
    photo = models.ImageField(upload_to='photos', blank=True)

    def __str__(self):
        """Returns a string with the car details."""
        return "[Car {}: {} {}]".format(self.registration_number,
                                        self.make, self.model)


class Reservation(models.Model):
    customer = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 related_name='reservations')

    # TODO: if we want to keep reservations history then on_delete=models.CASCADE below is not good
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        """Returns a string with the reservation details."""
        return "[Reservation {}. Customer: {}, car: {}, from: {}, to: {}]".format(
                self.id, self.customer, self.car, self.start, self.end)

