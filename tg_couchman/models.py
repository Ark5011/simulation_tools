from django.db import models
from django.contrib.auth.models import User
    
class Formulation(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.CharField(max_length=100)
    water_min = models.FloatField()
    casein = models.FloatField()
    whey_protein = models.FloatField()
    lactose = models.FloatField()
    GOS = models.FloatField()
    PDX = models.FloatField()
    
