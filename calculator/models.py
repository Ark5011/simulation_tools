from django.conf import settings
from django.db import models
from django.utils import timezone


class Tg(models.Model):
    water = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()

    # def __str__(self):
    #     return self.title

class Cp(models.Model):
    water = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()
    
class Formulation(models.Model):
    water = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()