from django.db import models

class Car(models.Model):
    """
    Represents a car owned by the car rental company.
    """
    registration_number = models.CharField(max_length=10, blank=False, unique=True)
    make = models.CharField(max_length=255, blank=False)
    model = models.CharField(max_length=255, blank=False)

    def __str__(self):
        """Returns a string with the car details."""
        return "[Car {}: {} {}]".format(self.registration_number,
                                        self.make, self.model)
