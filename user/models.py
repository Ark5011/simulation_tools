from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    factory = models.CharField(max_length=200)
    line = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    location_choices = models.CharField(max_length=200)
    LOCATION_CHOICES = (
    ("PLANT", "Plant"),
    ("PILOT PLANT", "Pilot Plant"),
    )

    location = models.CharField(max_length=12,
                    choices=LOCATION_CHOICES,
                    default="PLANT")